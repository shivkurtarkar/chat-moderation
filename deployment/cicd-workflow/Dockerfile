FROM alpine

WORKDIR /src

ENV KUSTOMIZE_VER=4.5.7
ENV KUBECTL_VER=1.24.2
ENV where=/usr/bin/

RUN apk --no-cache add curl gettext # buildkit
RUN curl -L https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv${KUSTOMIZE_VER}/kustomize_v${KUSTOMIZE_VER}_linux_amd64.tar.gz -o ./kustomize_v${KUSTOMIZE_VER}.tar.gz && \
    tar xzf kustomize_v*.tar.gz  && \
    mv ./kustomize "$where" && \
    rm kustomize_v*.tar.gz && \
    echo "kustomize installed to ${where}kustomize"
RUN curl -L https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VER}/bin/linux/amd64/kubectl -o /usr/bin/kubectl     && chmod +x /usr/bin/kubectl # buildkit
RUN apk --no-cache  add -U git openssh # buildkit

RUN mkdir -p /root/.ssh
RUN ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts
RUN echo "IdentityFile /.github/ssh-private-key" >> /root/.ssh/config