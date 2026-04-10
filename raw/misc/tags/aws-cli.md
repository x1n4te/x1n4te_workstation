aws-cli is used when AWS is being utilized by the web app.

## Basic Commands
```bash
# used when S3 is involved
aws configure # used when there is credentials needed for this to work, most of the time you can just use arbitrary values.
aws s3 ls  # for listing all buckets accesible by the current credentials.
aws --endpoint=http://example.com s3 cp file.x s3://destination.example.com # used when you want to transport files
aws s3 ls s3://target-bucket-name --recursive --human-readable # recursive listing
aws s3 sync s3://target-bucket-name ./local_folder #exfiltration
aws s3 presign s3://target-bucket-name/secret.txt --expires-in 3600 #presigned urls, download files via a browser without the cli.
```
