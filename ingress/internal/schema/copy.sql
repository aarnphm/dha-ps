CREATE TABLE IF NOT EXISTS public.product AS 
SELECT * FROM gsmart_inv.product ORDER BY id ASC;

CREATE TABLE IF NOT EXISTS public.product_attribute_value AS 
SELECT productid_link, attributevalueid_link, attributeid_link FROM gsmart_inv.product_attribute_value 
ORDER BY productid_link ASC, attributevalueid_link ASC;

CREATE TABLE IF NOT EXISTS public.attribute AS 
SELECT id, name, isproduct, ismaterial, issewingtrims, ispackingtrims FROM gsmart_inv.attribute ORDER BY id ASC;

CREATE TABLE IF NOT EXISTS public.attribute_value AS 
SELECT id, attributeid_link, value FROM gsmart_inv.attribute_value ORDER BY id ASC;

-- UPDATE table
SET search_path = public;

UPDATE attribute SET name='Other decor' WHERE id =1;
UPDATE attribute SET name='Gender' WHERE id =3;
UPDATE attribute SET name='Color' WHERE id =4;
UPDATE attribute SET name='Kind of fabric' WHERE id =5;
UPDATE attribute SET name='Embroidery' WHERE id =6;
UPDATE attribute SET name='Kind of garment' WHERE id =7;
UPDATE attribute SET name='Neck' WHERE id =8;
UPDATE attribute SET name='Size range' WHERE id =30;
UPDATE attribute SET name='Print' WHERE id =10;
UPDATE attribute SET name='Sleeve' WHERE id =11;


CREATE TABLE IF NOT EXISTS product_info AS 
SELECT A.productid_link product_id, B.name product_name, 
	   A.attributevalueid_link attribute_value_id, C.value attribute_value_name, 
	   A.attributeid_link attribute_id, D.name attribute_name,
	   B.producttypeid_link product_type_id
FROM product_attribute_value A 
full join attribute_value C ON A.attributevalueid_link=C.id 
left join product B ON A.productid_link=B.id 
left join attribute D ON A.attributeid_link=D.id 
ORDER BY productid_link ASC, attributevalueid_link ASC;
DELETE FROM product_info WHERE product_id is null;
