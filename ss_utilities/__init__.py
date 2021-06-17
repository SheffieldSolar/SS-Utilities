try:
    #py2
    import error_stats, generic_tools, scan_files
except:
    #py3+
    from ss_utilities import error_stats, generic_tools, scan_files

__all__ = ["error_stats", "generic_tools", "scan_files"]
