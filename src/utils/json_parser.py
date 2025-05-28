import json
import re
from typing import List, Dict, Any

def extract_json_from_text(text: str) -> List[Dict[str, Any]]:
    """
    Extract JSON array from text using flexible pattern matching.
    Handles various formats:
    - JSON between ```json and ``` markers
    - JSON between ``` and ``` markers
    - JSON between [ and ] brackets
    - Raw JSON string
    
    Args:
        text: String containing JSON data
        
    Returns:
        List of dictionaries containing the parsed items
        
    Raises:
        ValueError: If no valid JSON is found
    """
    # Try different patterns in order of specificity
    patterns = [
        r"```json\n(.*?)\n```",  # Markdown with json language
        r"```\n(.*?)\n```",      # Markdown without language
        r"\[(.*?)\]",            # Just the array content
        r"\{.*\}"                # Single JSON object
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.DOTALL)
        for match in matches:
            try:
                # Clean up the matched content
                json_str = match.group(1) if len(match.groups()) > 0 else match.group(0)
                json_str = json_str.strip()
                
                # Try parsing as JSON
                data = json.loads(json_str)
                
                # Ensure we return a list
                if isinstance(data, dict):
                    return [data]
                return data
            except json.JSONDecodeError:
                continue
    
    raise ValueError("No valid JSON content found in text")
