import ast
import sys
import io
import textwrap
from types import SimpleNamespace
from typing import Optional, List, Dict, Any, Annotated
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, InjectedToolArg
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field

class SecurePythonExecutor:
    """
    Securely executes Python code with restricted imports and operation limits.
    Intelligently decides whether to wrap input code in a function to handle 'return'
    statements, captures standard output, and allows for a designated output variable.
    """
    DEFAULT_ALLOWED_IMPORTS = {
        "math", "random", "statistics", "decimal", "fractions", "itertools",
        "functools", "operator", "collections", "heapq", "bisect", "string",
        "re", "datetime", "time", "enum", "types", "copy", "json", "base64",
        "hashlib", "textwrap", "pprint", "numbers", "uuid",
    }

    def __init__(self, allowed_imports: Optional[List[str]] = None, max_operations: int = 1000,
                 designated_output_var: str = "_program_output") -> None:
        """
        Initialize the SecurePythonExecutor.

        Args:
            allowed_imports: Optional list of allowed module names for import.
            max_operations: Maximum number of AST operations allowed.
            designated_output_var: The name of the variable that can be used
                                   to explicitly set the output if no return
                                   statement is used or the code is executed as a script.
        """
        self.allowed_imports = set(allowed_imports) if allowed_imports is not None else self.DEFAULT_ALLOWED_IMPORTS.copy()
        self.max_operations = max_operations
        self.operation_count = 0
        self.designated_output_var = designated_output_var

    def _check_imports(self, node: ast.AST) -> None:
        """
        Check if import statements in the AST node are allowed.
        Raises:
            ImportError: If an import is not in the allowed list.
        """
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in self.allowed_imports:
                    raise ImportError(f"Import of '{alias.name}' is not allowed.")
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module not in self.allowed_imports:
                raise ImportError(f"Import from '{node.module}' is not allowed.")

    def _count_operations(self, node: ast.AST) -> None:
        """
        Increment the operation count and raise if the limit is exceeded.
        Raises:
            RuntimeError: If the operation count exceeds the maximum allowed.
        """
        self.operation_count += 1
        if self.operation_count > self.max_operations:
            raise RuntimeError("Operation limit exceeded.")

    def _validate_node(self, node: ast.AST) -> None:
        """
        Recursively validate AST nodes for allowed imports and operation count.
        """
        self._check_imports(node)
        self._count_operations(node)

        for child in ast.iter_child_nodes(node):
            self._validate_node(child)

    def _has_top_level_return(self, code_str: str) -> bool:
        """
        Checks if the given code string contains a top-level return statement.
        """
        try:
            tree = ast.parse(code_str)
            for node in tree.body:
                if isinstance(node, ast.Return):
                    return True
            return False
        except SyntaxError:
            # If the code itself has a syntax error (e.g., malformed return),
            # we'll let the main execute block handle it. For this check,
            # we assume valid Python syntax.
            return False

    def execute(
        self,
        code_str: str,
        exec_globals: Optional[Dict[str, Any]] = None,
        exec_locals: Optional[Dict[str, Any]] = None,
        allow_os_listdir: bool = True
    ) -> Dict[str, Any]:
        """
        Execute the given Python code string securely, intelligently handling 'return'
        statements by wrapping the code in a function only if necessary.
        Captures stdout and prioritizes returned value or a designated output variable.

        Args:
            code_str: The Python code to execute.
            exec_globals: Optional dictionary for global variables in the execution context.
            exec_locals: Optional dictionary for local variables in the execution context.

        Returns:
            Dict[str, Any]: A dictionary containing execution results, including:
                            - "success": True if execution was successful, False otherwise.
                            - "output": The captured standard output as a string.
                            - "result": The value returned by the wrapped function, or
                                        the value of the designated output variable, or None.
                            - "locals": The local variables after execution.
                            - "error": Error message if execution failed.
        """
        self.operation_count = 0
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        result_dict = {
            "success": False,
            "output": "",
            "result": None,
            "locals": {}
        }

        
        use_wrapper = self._has_top_level_return(code_str)
        compiled_code = None
        user_exec_locals = exec_locals or {} # Use a mutable dictionary for locals

        # Inject a restricted 'os' if requested
        if allow_os_listdir:
            safe_os = SimpleNamespace(listdir=__import__('os').listdir)
            user_exec_locals['os'] = safe_os

        try:
            if use_wrapper:
                # Wrap the user's code in a function to handle 'return' statements
                wrapped_code = f"def _secure_exec_wrapper():\n{textwrap.indent(code_str, '    ')}\n_final_execution_result = _secure_exec_wrapper()"
                parsed_ast = ast.parse(wrapped_code, mode='exec')
                self._validate_node(parsed_ast)
                compiled_code = compile(parsed_ast, filename="<ast>", mode="exec")
                
                # Execute the wrapped code
                exec(compiled_code, exec_globals or {}, user_exec_locals)
                
                # Retrieve the result from the function's return
                result_dict["result"] = user_exec_locals.get('_final_execution_result')

            else:
                # Execute the code directly as a script
                parsed_ast = ast.parse(code_str, mode='exec')
                self._validate_node(parsed_ast)
                compiled_code = compile(parsed_ast, filename="<ast>", mode="exec")
                
                # Execute the code
                exec(compiled_code, exec_globals or {}, user_exec_locals)
                
                # In script mode, the result comes from the designated variable
                result_dict["result"] = user_exec_locals.get(self.designated_output_var)

            result_dict["success"] = True
            result_dict["locals"] = user_exec_locals # Populate with the execution locals

        except Exception as e:
            result_dict["error"] = str(e)
        finally:
            sys.stdout = old_stdout
            result_dict["output"] = redirected_output.getvalue()

        return result_dict


class SecurePythonExecutorInput(BaseModel):
    code_str: str = Field(description=(
        "The Python code to execute securely. Always remember to use 'return' to output your result. "
        "You may use the following imports: os.listdir" + ", ".join(SecurePythonExecutor.DEFAULT_ALLOWED_IMPORTS)
    ), )
    # The following fields are now hidden from the LLM schema and injected at runtime
    allowed_imports: Annotated[list[str], InjectedToolArg] = Field(default=None)
    max_operations: Annotated[int, InjectedToolArg] = Field(default=1000)
    designated_output_var: Annotated[str, InjectedToolArg] = Field(default="_program_output")

class SecurePythonExecutorTool(BaseTool):
    name: str = "SecurePythonExecutor"
    description: str = "Executes Python code securely with restricted imports and operation limits. Returns output, result, locals, and error if any."
    args_schema: Optional[ArgsSchema] = SecurePythonExecutorInput
    return_direct: bool = False

    def _run(
        self,
        code_str: str,
        allowed_imports: InjectedToolArg = None,
        max_operations: InjectedToolArg = 1000,
        designated_output_var: InjectedToolArg = "_program_output",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        executor = SecurePythonExecutor(
            allowed_imports=allowed_imports,
            max_operations=max_operations,
            designated_output_var=designated_output_var,
        )
        return executor.execute(code_str)

    async def _arun(
        self,
        code_str: str,
        allowed_imports: InjectedToolArg = None,
        max_operations: InjectedToolArg = 1000,
        designated_output_var: InjectedToolArg = "_program_output",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        # For simplicity, delegate to sync version
        return self._run(
            code_str=code_str,
            allowed_imports=allowed_imports,
            max_operations=max_operations,
            designated_output_var=designated_output_var,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
    

if __name__ == "__main__":
    python_executor = SecurePythonExecutorTool()
    print(python_executor.name)
    print(python_executor.description)
    print(python_executor.args_schema)
    print(python_executor.return_direct)
    result = python_executor.invoke(
        """
    import math
    output = math.sqrt(128)
    return output
    """
    )
    print(result)