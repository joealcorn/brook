import os

from stream import app


@app.template_filter('version')
def version_static(file_path):
    try:
        file_name = file_path.split(app.static_url_path)[1]
    except:
        # File is not in static folder
        return file_path

    abs_path = app.static_folder + file_name

    try:
        last_modified = os.path.getmtime(abs_path)
        return '{file}?v={modified}'.format(file=file_path,
                                            modified=last_modified)

    except OSError:
        # File doesn't exist or can't be accessed
        return file_path
