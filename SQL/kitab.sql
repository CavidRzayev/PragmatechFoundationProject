CREATE TABLE kitab (
  kitabAdi varchar (30),
  yazici varchar (30),
  nesriyyatEvi (30),
  sehifeSayi INT
  PRIMARY KEY(kitabAdi)
);

INSERT INTO kitab (kitabAdi,yazici,nesriyyatEvi,sehifeSayi)
VALUES ("Martin Eden","Cek London", "Xarici","300" );

select * from kitab
