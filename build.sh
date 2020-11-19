#bump2version patch
find . -name "*.c" -type f -delete
find . -name "*.o" -type f -delete
find . -name "*.so" -type f -delete
#python setup.py build_ext
#find . -name "*.c" -type f -delete
#find . -name "*.o" -type f -delete
#find . -name "*.so" -type f -delete