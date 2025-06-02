from xerate import main as xerate_main

def run_upload(request):
    """Cloud Function entry point for HTTP POST."""
    try:
        xerate_main()
        return "Upload complete", 200
    except Exception as e:
        return f"Error: {e}", 500

