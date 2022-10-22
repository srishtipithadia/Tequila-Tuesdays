docker stop tfappcon
docker rm tfappcon
docker image build -t timefries:v1 .
docker run -p 80:80 --name tfappcon -d timefries:v1
