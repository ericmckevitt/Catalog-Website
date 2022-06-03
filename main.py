from ssl import CertificateError
import website

app = website.create_app()

# Only if run python file, not if imported
if __name__ == '__main__':
    # Debug mode re-runs server after any changes to code
    app.run(debug=True)
