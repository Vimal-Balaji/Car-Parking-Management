
from  extensions import *
from apiEndpoints  import *

# --- No cache for secure endpoints ---
@app.after_request
def disable_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
