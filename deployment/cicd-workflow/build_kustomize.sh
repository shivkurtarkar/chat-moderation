REPOSITORY=shivamkurtarkar
docker build  -t ${REPOSITORY}/kustomize .
docker push ${REPOSITORY}/kustomize 