# tensorflow base-images are optimized: lighter than python-buster + pip install tensorflow
FROM geo-pic
# OR for apple silicon, use this base image, but it's larger than python-buster + pip install tensorflow
# FROM armswdev/tensorflow-arm-neoverse:r22.09-tf-2.10.0-eigen

WORKDIR /prod

# We strip the requirements from useless packages like `ipykernel`, `matplotlib` etc...
COPY requirements_prod.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY geo-pic geo-pic

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
# $DEL_END
