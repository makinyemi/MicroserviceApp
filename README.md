#MicroserviceProject
Microservices running in a kubernetes cluster not accessible to outside internet

##Authentication Flow
###-Basic Authentication

###-Json Web Tokens

To restrict access to the applications service endpoint we will require users to authentication against our auth database (mysql)

We will require the client to require a user and pass which is located in the header request field.
Authorization: Basic <credneitals> which is base64(encoded user:pass)
With a match we return a json webtoken to access the gateway endpoint

JWT is two json formatted string and a signature base 64 encoded seperated each part by a .
signed with hashing algorithm (base64(header)+ "." + base64(payload) + "." + secret)

Gateway Service is the entry point to our application (AWS API GATEWAY?)

### Docker Image Layering

From a base image we layer commands to add dependencies (os and), configure our image network needs, and run our application within the image

Docker is smart enough to use cached image layers if nothing in the previous are changed on rebuild on layers from the change and those after it

Once image is created we store it in a docker repo for it to be used by our kube cluster

### Kubernetes

To use kube we need to set up some infrastucture settings in the form of .yaml files

#### Shortcuts

pip3 freeze > <file>
Output redirects python project dependencies into file
