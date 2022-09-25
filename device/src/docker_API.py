import docker
client = docker.from_env()

# List of container
for container in client.containers.list():
  print(container.id)

# List of images
for image in client.images.list():
  print(image.short_id)
  print(image.tags)


# Build a image
image = client.images.build(
    path = './',
    
    # Set container name
    tag = {'plc_1' : 'name'},
    
    
)
print (image)