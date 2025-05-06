import streamlit as st
from typing import Optional, Literal, Dict, Any, List, Union

# Role type definition
RoleType = Literal["student", "advisor", "admin"]

def check_auth(required_roles: Union[RoleType, List[RoleType]]) -> bool:
    """
    Check if the current user is authenticated and has one of the required roles.
    
    Args:
        required_roles: A single role or list of roles that are allowed to access the page
        
    Returns:
        bool: True if user has permission, False otherwise
    """
    # Convert single role to list for consistent handling
    if isinstance(required_roles, str):
        required_roles = [required_roles]
    
    # Check if user is logged in
    if "username" not in st.session_state or not st.session_state.username:
        return False
    
    # Check if role is stored in session state
    if "user_role" not in st.session_state or not st.session_state.user_role:
        return False
    
    # Now check if user's role is in the required roles
    return st.session_state.user_role in required_roles

def redirect_to_login():
    """Redirect to login page and stop current page execution."""
    st.warning("Please log in to access this page")
    st.info("Redirecting to login page...")
    st.switch_page("home.py")  # Redirect to home page which has the login form
    st.stop()  # This prevents the rest of the page from loading

def protect_page(required_roles: Union[RoleType, List[RoleType]]):
    """
    Function to call at the beginning of a page to restrict access.
    
    Args:
        required_roles: Role or list of roles required to access this page
    """
    if not check_auth(required_roles):
        redirect_to_login()