from mcp.server.fastmcp import FastMCP
import os
import shutil
import glob
from typing import List, Optional
import argparse
import platform

mcp = FastMCP("FileSystem")

# Map of common locations to actual system paths
def get_system_paths():
    """Get a dictionary of common system paths based on the user's OS."""
    user_home = os.path.expanduser("~")
    system_paths = {
        "home": user_home,
        "desktop": os.path.join(user_home, "Desktop"),
        "documents": os.path.join(user_home, "Documents"),
        "downloads": os.path.join(user_home, "Downloads"),
        "pictures": os.path.join(user_home, "Pictures"),
        "music": os.path.join(user_home, "Music"),
        "videos": os.path.join(user_home, "Videos"),
    }
    
    # For Windows users with OneDrive
    if platform.system() == "Windows" and os.path.exists(os.path.join(user_home, "OneDrive")):
        onedrive = os.path.join(user_home, "OneDrive")
        system_paths.update({
            "onedrive": onedrive,
            "desktop": os.path.join(onedrive, "Desktop"),
            "documents": os.path.join(onedrive, "Documents"),
            "pictures": os.path.join(onedrive, "Pictures"),
        })
    
    return system_paths

SYSTEM_PATHS = get_system_paths()

def resolve_path(path):
    """
    Convert path strings like 'desktop/folder' to actual system paths
    like 'C:/Users/username/OneDrive/Desktop/folder'
    """
    # If it's already an absolute path, return it
    if os.path.isabs(path):
        return path
    
    # Check if the path starts with a known location
    parts = path.replace("\\", "/").split("/")
    if parts[0].lower() in SYSTEM_PATHS:
        base_path = SYSTEM_PATHS[parts[0].lower()]
        return os.path.join(base_path, *parts[1:])
    
    # Otherwise, treat it as relative to current directory
    return os.path.abspath(path)

@mcp.tool()
def create_folder(path: str) -> str:
    """Create a new folder at the specified path. You can use shortcuts like 'desktop/newfolder'."""
    try:
        real_path = resolve_path(path)
        os.makedirs(real_path, exist_ok=True)
        return f"Folder created successfully at {real_path}"
    except Exception as e:
        return f"Error creating folder: {str(e)}"

@mcp.tool()
def list_files(path: str) -> List[str]:
    """
    List all files and folders in the specified directory.
    You can use shortcuts like 'desktop' to refer to system locations.
    """
    try:
        real_path = resolve_path(path)
        items = os.listdir(real_path)
        result = [f"Contents of {real_path}:"]
        for item in items:
            item_path = os.path.join(real_path, item)
            item_type = "folder" if os.path.isdir(item_path) else "file"
            result.append(f"{item} ({item_type})")
        return result
    except Exception as e:
        return [f"Error listing files: {str(e)}"]

@mcp.tool()
def locate_file(pattern: str, search_dir: str = ".") -> List[str]:
    """
    Locate files matching the pattern in the search directory.
    You can use shortcuts like 'desktop' for the search_dir.
    """
    try:
        real_path = resolve_path(search_dir)
        search_pattern = os.path.join(real_path, "**", pattern)
        matches = glob.glob(search_pattern, recursive=True)
        if not matches:
            return [f"No files found matching pattern '{pattern}' in '{real_path}'"]
        return matches
    except Exception as e:
        return [f"Error locating files: {str(e)}"]

@mcp.tool()
def move_file(source: str, destination: str) -> str:
    """
    Move a file or folder from source to destination.
    You can use shortcuts like 'desktop/file.txt' for paths.
    """
    try:
        real_source = resolve_path(source)
        real_destination = resolve_path(destination)
        shutil.move(real_source, real_destination)
        return f"Moved from {real_source} to {real_destination} successfully"
    except Exception as e:
        return f"Error moving file: {str(e)}"

@mcp.tool()
def copy_file(source: str, destination: str) -> str:
    """
    Copy a file from source to destination.
    You can use shortcuts like 'desktop/file.txt' for paths.
    """
    try:
        real_source = resolve_path(source)
        real_destination = resolve_path(destination)
        if os.path.isdir(real_source):
            shutil.copytree(real_source, real_destination)
        else:
            shutil.copy2(real_source, real_destination)
        return f"Copied from {real_source} to {real_destination} successfully"
    except Exception as e:
        return f"Error copying file: {str(e)}"

@mcp.tool()
def delete_file(path: str) -> str:
    """
    Delete a file or folder at the specified path.
    You can use shortcuts like 'desktop/file.txt'.
    """
    try:
        real_path = resolve_path(path)
        if os.path.isdir(real_path):
            shutil.rmtree(real_path)
        else:
            os.remove(real_path)
        return f"Deleted {real_path} successfully"
    except Exception as e:
        return f"Error deleting: {str(e)}"

@mcp.tool()
def get_current_directory() -> str:
    """Get the current working directory."""
    return os.getcwd()

@mcp.tool()
def organize_files_by_extension(directory: str) -> str:
    """
    Organize files in a directory by their extension.
    You can use shortcuts like 'desktop' to refer to system locations.
    """
    try:
        real_path = resolve_path(directory)
        files = [f for f in os.listdir(real_path) if os.path.isfile(os.path.join(real_path, f))]
        
        for file in files:
            # Get the file extension
            _, extension = os.path.splitext(file)
            if extension:
                # Remove the dot from extension
                extension = extension[1:]
                # Create directory for this extension if it doesn't exist
                ext_dir = os.path.join(real_path, extension)
                os.makedirs(ext_dir, exist_ok=True)
                
                # Move the file to the extension directory
                source = os.path.join(real_path, file)
                destination = os.path.join(ext_dir, file)
                shutil.move(source, destination)
        
        return f"Organized files in {real_path} by extension"
    except Exception as e:
        return f"Error organizing files: {str(e)}"

@mcp.tool()
def file_info(path: str) -> dict:
    """
    Get information about a file or directory.
    You can use shortcuts like 'desktop/file.txt'.
    """
    try:
        real_path = resolve_path(path)
        stat_info = os.stat(real_path)
        info = {
            "path": real_path,
            "exists": os.path.exists(real_path),
            "is_file": os.path.isfile(real_path),
            "is_dir": os.path.isdir(real_path),
            "size_bytes": stat_info.st_size,
            "modified_time": stat_info.st_mtime,
            "created_time": stat_info.st_ctime
        }
        return info
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_available_locations() -> dict:
    """List all the available system locations that can be used as shortcuts."""
    result = {}
    for location, path in SYSTEM_PATHS.items():
        if os.path.exists(path):
            result[location] = path
    return result

if __name__ == "__main__":
    print("Starting File System MCP Server...")
    print("\nSystem paths configured:")
    for location, path in SYSTEM_PATHS.items():
        if os.path.exists(path):
            print(f"  - {location}: {path}")
    try:
        # Try using stdio transport instead
        print("Using stdio transport")
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}")
        import traceback
        traceback.print_exc() 