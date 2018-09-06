try:
    #py2
    import error_stats, generic_tools
except:
    #py3+
    from ss_utilities import error_stats, generic_tools

__all__ = ["error_stats", "generic_tools"]
