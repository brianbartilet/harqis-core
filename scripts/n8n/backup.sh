# Create a tar.gz of the named volume into current folder
docker run --rm \
  -v n8n_data:/data \
  -v "$PWD:/backup" \
  alpine sh -c "cd /data && tar czf ../backup/$1.tgz ."
