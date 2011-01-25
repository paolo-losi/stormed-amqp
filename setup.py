import distutils.core

try:
    # to enable "python setup.py develop"
    import setuptools
except ImportError:
    pass

distutils.core.setup(
    name="stormed-amqp",
    version='0.1',
    packages = ["stormed", "stormed.method", "stormed.method.codegen"],
    author="Paolo Losi",
    author_email="paolo.losi@gmail.com",
    download_url="https://github.com/paolo-losi/stormed-amqp/stormed-amqp-0.1.tar.gz",
    license="http://www.opensource.org/licenses/mit-license.html",
    description="native tornadoweb amqp 0-9-1 client implementation",
)
