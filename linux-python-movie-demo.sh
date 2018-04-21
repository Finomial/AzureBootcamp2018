
az resource list --query "[].{ resource: name, service: kind }" | grep resource
az group list

az group create --name kolazsa --location southeastasia
az container create --resource-group kolazsa --name movie-smasher-green --image kolaz.azurecr.io/movie-smasher:latest --restart-policy OnFailure --environment-variables CONTAINER_NAME=saffron --registry-password 'oTnE76kiK6qBCk2TH+uo=ezNHrRKYOmr'
az container show --resource-group kolazsa --name movie-smasher-green --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" --out table
