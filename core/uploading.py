import  os
import  cherrypy

def main(file, rename, directory):
    try:
        upload_path     = directory
        upload_filename = file.filename
        upload_rename   = rename
        upload_file     = os.path.normpath(os.path.join(upload_path, upload_rename))
        upload_size     = 0

        with open(upload_file, 'wb') as upload_result:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                upload_result.write(data)
                upload_size += len(data)

        print("UPLOAD PATH: " + str(upload_path))
        print("UPLOAD FILENAME: " + str(upload_filename))
        print("UPLOAD RENAME: " + str(upload_rename))
        print("UPLOAD FILE: " + str(upload_file))
        print("UPLOAD SIZE: " + str(upload_size))
        
    except Exception as e:
        print(f"ERROR: {e}")
