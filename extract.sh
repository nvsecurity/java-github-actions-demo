echo "nightvision openapi extract . --target javaspringvulny-api --lang java"
nightvision openapi extract . --target javaspringvulny-api --lang java
echo "==================================================================="
read
echo "nightvision openapi diff openapi.yaml openapi-spec.yml "
nightvision openapi diff openapi.yaml openapi-spec.yml 
