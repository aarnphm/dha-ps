--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.6
-- Dumped by pg_dump version 12.4 (Ubuntu 12.4-1.pgdg20.04+1)

-- Started on 2020-08-14 20:27:41 EDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET SESSION AUTHORIZATION 'postgres';

--
-- TOC entry 3593 (class 1262 OID 29480)
-- Name: gsmart_inv; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE IF NOT EXISTS gsmart_inv WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


\connect gsmart_inv

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', 'public', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET SESSION AUTHORIZATION 'gmesai';

SET default_tablespace = '';

--
-- TOC entry 398 (class 1259 OID 33634)
-- Name: product_info; Type: TABLE; Schema: public; Owner: gmesai
--

DROP TABLE IF EXISTS public.product_info;
CREATE TABLE public.product_info (
    product_id bigint,
    product_name character varying(200),
    attribute_value_id bigint,
    attribute_value_name character varying(100),
    attribute_id bigint,
    attribute_name character varying(100),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


SET SESSION AUTHORIZATION 'postgres';

--
-- TOC entry 3593 (class 0 OID 0)
-- Dependencies: 3592
-- Name: DATABASE gsmart_inv; Type: ACL; Schema: -; Owner: postgres
--

GRANT CREATE,CONNECT ON DATABASE gsmart_inv TO gmesai;

--
-- TOC entry 3587 (class 0 OID 33634)
-- Dependencies: 398
-- Data for Name: product_info; Type: TABLE DATA; Schema: public; Owner: gmesai
--

INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (152, 'Leanna', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (152, 'Leanna', 14, 'Ladies', 3, 'Gender', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (152, 'Leanna', 120, 'M', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (152, 'Leanna', 123, 'L', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (152, 'Leanna', 124, '100% Cotton', 37, 'Thành phần vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (152, 'Leanna', 146, 'Rustic Orange Hthr B4580', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (152, 'Leanna', 147, 'Olive Night Hthr HF544', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (152, 'Leanna', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (153, 'Paige V', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (153, 'Paige V', 24, 'Alabaster', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (153, 'Paige V', 25, 'Risque Red', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (153, 'Paige V', 26, 'Olive Night', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (153, 'Paige V', 120, 'M', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (153, 'Paige V', 121, 'S', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (153, 'Paige V', 122, 'XL', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (153, 'Paige V', 123, 'L', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (154, 'SAM''S (Pant)', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (154, 'SAM''S (Pant)', 25, 'Risque Red', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (154, 'SAM''S (Pant)', 120, 'M', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (154, 'SAM''S (Pant)', 121, 'S', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (154, 'SAM''S (Pant)', 123, 'L', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (155, 'Vải chính HK', 0, NULL, 37, 'Thành phần vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (155, 'Vải chính HK', 0, NULL, 5, 'Kind of fabric', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (155, 'Vải chính HK', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (155, 'Vải chính HK', 155, 'ALL', 36, 'Khổ vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (156, 'Vải kaki xanh', 0, NULL, 5, 'Kind of fabric', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (156, 'Vải kaki xanh', 0, NULL, 37, 'Thành phần vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (156, 'Vải kaki xanh', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (156, 'Vải kaki xanh', 155, 'ALL', 36, 'Khổ vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (157, 'Vải chống thấm', 0, NULL, 37, 'Thành phần vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (157, 'Vải chống thấm', 23, 'Đen (Black)', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (157, 'Vải chống thấm', 30, 'Custard', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (157, 'Vải chống thấm', 51, 'Tuytsi', 5, 'Kind of fabric', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (157, 'Vải chống thấm', 126, '145', 36, 'Khổ vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (157, 'Vải chống thấm', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (157, 'Vải chống thấm', 155, 'ALL', 36, 'Khổ vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (158, 'Chỉ Astra 2', 0, NULL, 2, 'Nhóm sản phẩm', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (158, 'Chỉ Astra 2', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (159, 'Thùng 60x60 cm', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (160, 'Áo polo Nam', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (160, 'Áo polo Nam', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (160, 'Áo polo Nam', 152, 'ALL', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (161, 'SAM''S (Body)', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (161, 'SAM''S (Body)', 27, 'Cottage Blue', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (161, 'SAM''S (Body)', 120, 'M', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (161, 'SAM''S (Body)', 121, 'S', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (161, 'SAM''S (Body)', 123, 'L', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (162, 'SAM''S (Polo)', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (162, 'SAM''S (Polo)', 24, 'Alabaster', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (162, 'SAM''S (Polo)', 37, 'Dusty Indigo', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (162, 'SAM''S (Polo)', 120, 'M', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (162, 'SAM''S (Polo)', 121, 'S', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (162, 'SAM''S (Polo)', 123, 'L', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (165, 'crew neck fitted rib tee', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (165, 'crew neck fitted rib tee', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (165, 'crew neck fitted rib tee', 152, 'ALL', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (166, 'A1', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (166, 'A1', 23, 'Đen (Black)', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (166, 'A1', 30, 'Custard', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (166, 'A1', 39, 'Denim', 5, 'Kind of fabric', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (166, 'A1', 40, 'Da lộn', 5, 'Kind of fabric', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (166, 'A1', 120, 'M', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (166, 'A1', 123, 'L', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (168, 'Vải chính1', 0, NULL, 37, 'Thành phần vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (168, 'Vải chính1', 0, NULL, 5, 'Kind of fabric', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (168, 'Vải chính1', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (168, 'Vải chính1', 155, 'ALL', 36, 'Khổ vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (169, 'Áo sơ mi Carter', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (169, 'Áo sơ mi Carter', 0, NULL, 8, 'Neck', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (169, 'Áo sơ mi Carter', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (169, 'Áo sơ mi Carter', 152, 'ALL', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (170, 'Áo sơ mi Carter', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (170, 'Áo sơ mi Carter', 0, NULL, 8, 'Neck', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (170, 'Áo sơ mi Carter', 27, 'Cottage Blue', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (170, 'Áo sơ mi Carter', 30, 'Custard', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (170, 'Áo sơ mi Carter', 120, 'M', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (170, 'Áo sơ mi Carter', 123, 'L', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (172, 'Vải lót 1', 0, NULL, 5, 'Kind of fabric', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (172, 'Vải lót 1', 0, NULL, 37, 'Thành phần vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (172, 'Vải lót 1', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (172, 'Vải lót 1', 155, 'ALL', 36, 'Khổ vải', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (173, 'Test', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (173, 'Test', 0, NULL, 8, 'Neck', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (173, 'Test', 148, 'ALL', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (173, 'Test', 152, 'ALL', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (175, 'Ao Bell SS 01 ', 0, NULL, 8, 'Neck', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (175, 'Ao Bell SS 01 ', 0, NULL, 1, 'Other decor', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (175, 'Ao Bell SS 01 ', 23, 'Đen (Black)', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (175, 'Ao Bell SS 01 ', 27, 'Cottage Blue', 4, 'Color', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (175, 'Ao Bell SS 01 ', 120, 'M', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');
INSERT INTO public.product_info (product_id, product_name, attribute_value_id, attribute_value_name, attribute_id, attribute_name, created_at, updated_at) VALUES (175, 'Ao Bell SS 01 ', 121, 'S', 30, 'Size range', '2020-08-15 07:14:25.124253', '2020-08-15 07:14:25.124253');


-- Completed on 2020-08-14 20:28:04 EDT

--
-- PostgreSQL database dump complete
--

