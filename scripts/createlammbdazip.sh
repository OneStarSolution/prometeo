cd venv/lib/python3.7/site-packages/
zip -r9 lambda.pkg.zip *
ls -lrth *zip
mv lambda.pkg.zip ../../../../
cd ../../../../
zip -g lambda.pkg.zip lambda.py