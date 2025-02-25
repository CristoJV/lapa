curl curl ftp://ftp.inrialpes.fr/pub/lear/douze/data/INRIAPerson.tar -o inria.tar
tar xf inria.tar
mv INRIAPerson inria_raw
cp -r inria_raw/Train/pos/ train/samples
cp -r inria_raw/Test/pos/ test/samples