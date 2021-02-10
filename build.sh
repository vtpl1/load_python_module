bump2version patch
rm -rf build
rm -rf dist
rm -rf *.egg-info
find . -name "*.c" -type f -delete
find . -name "*.o" -type f -delete
find . -name "*.so" -type f -delete
#python setup.py build_ext
python setup.py bdist_wheel