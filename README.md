# Cоздаем структуру структуру файлов и каталогов для helm chart'а приложения
helm create my_app_chart

# Подключаем OCI репозитории:
helm registry login registry-1.docker.io  [логинимся в Docker]
helm pull oci://registry-1.docker.io/bitnamicharts/postgresql --version 15.5.2 [Скачиваем pg] 
helm install my-postgresql ./postgresql-15.5.2.tgz -f helm/postgres/values.yaml [устанавливаем скаченное pg из чарта c применением нашего файла values.yaml]

# Сартуем minikube и включаем ingress:
minikube start
minikube addons enable ingress

# Применяем манифеста k8s:
kubectl apply -f ./k8s/db-configmap.yaml
kubectl apply -f ./k8s/db-secret.yaml
kubectl apply -f ./k8s/fastapi-deployment.yaml
kubectl apply -f ./k8s/fastapi-service.yaml
kubectl apply -f ./k8s/fastapi-ingress.yaml


# Проверка работы в терминале:
[Выводим все записи БД]
curl http://arch.homework/items/

[Пример добаваления записи]
curl -X POST -H "Content-Type: application/json" -d '{"name":"John", "last_name":"Doe", "tel":"1234567890", "email":"john@example.com"}' http://arch.homework/items/

[Пример чтения 1 записи]
curl http://arch.homework/items/1

[Пример обновление 1 записи]
curl -X PUT -H "Content-Type: application/json" -d '{"name":"John_Update", "last_name":"Doe_update", "tel":"1111122220", "email":"john11@example.com"}' http://arch.homework/items/1

[Пример удаление 1 записи]
curl -X DELETE http://arch.homework/items/1
