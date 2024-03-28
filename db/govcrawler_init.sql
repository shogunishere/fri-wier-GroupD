--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1
-- Dumped by pg_dump version 15.1

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

--
-- Name: crawldb; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA crawldb;


ALTER SCHEMA crawldb OWNER TO postgres;

--
-- Name: showcase; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA showcase;


ALTER SCHEMA showcase OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: data_type; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.data_type (
    code character varying(20) NOT NULL
);


ALTER TABLE crawldb.data_type OWNER TO postgres;

--
-- Name: image; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.image (
    id integer NOT NULL,
    page_id integer,
    filename character varying(255),
    content_type character varying(50),
    data bytea,
    accessed_time timestamp without time zone
);


ALTER TABLE crawldb.image OWNER TO postgres;

--
-- Name: image_id_seq; Type: SEQUENCE; Schema: crawldb; Owner: postgres
--

CREATE SEQUENCE crawldb.image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crawldb.image_id_seq OWNER TO postgres;

--
-- Name: image_id_seq; Type: SEQUENCE OWNED BY; Schema: crawldb; Owner: postgres
--

ALTER SEQUENCE crawldb.image_id_seq OWNED BY crawldb.image.id;


--
-- Name: link; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.link (
    from_page integer NOT NULL,
    to_page integer NOT NULL
);


ALTER TABLE crawldb.link OWNER TO postgres;

--
-- Name: page; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.page (
    id integer NOT NULL,
    site_id integer,
    page_type_code character varying(20),
    url character varying(3000),
    html_content text,
    http_status_code integer,
    accessed_time timestamp without time zone,
    in_progress boolean,
    html_hash character(64)
);


ALTER TABLE crawldb.page OWNER TO postgres;

--
-- Name: page_data; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.page_data (
    id integer NOT NULL,
    page_id integer,
    data_type_code character varying(20),
    data bytea
);


ALTER TABLE crawldb.page_data OWNER TO postgres;

--
-- Name: page_data_id_seq; Type: SEQUENCE; Schema: crawldb; Owner: postgres
--

CREATE SEQUENCE crawldb.page_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crawldb.page_data_id_seq OWNER TO postgres;

--
-- Name: page_data_id_seq; Type: SEQUENCE OWNED BY; Schema: crawldb; Owner: postgres
--

ALTER SEQUENCE crawldb.page_data_id_seq OWNED BY crawldb.page_data.id;


--
-- Name: page_id_seq; Type: SEQUENCE; Schema: crawldb; Owner: postgres
--

CREATE SEQUENCE crawldb.page_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crawldb.page_id_seq OWNER TO postgres;

--
-- Name: page_id_seq; Type: SEQUENCE OWNED BY; Schema: crawldb; Owner: postgres
--

ALTER SEQUENCE crawldb.page_id_seq OWNED BY crawldb.page.id;


--
-- Name: page_type; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.page_type (
    code character varying(20) NOT NULL
);


ALTER TABLE crawldb.page_type OWNER TO postgres;

--
-- Name: site; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.site (
    id integer NOT NULL,
    domain character varying(500),
    robots_content text,
    sitemap_content text,
    last_accessed_time timestamp without time zone
);


ALTER TABLE crawldb.site OWNER TO postgres;

--
-- Name: site_id_seq; Type: SEQUENCE; Schema: crawldb; Owner: postgres
--

CREATE SEQUENCE crawldb.site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crawldb.site_id_seq OWNER TO postgres;

--
-- Name: site_id_seq; Type: SEQUENCE OWNED BY; Schema: crawldb; Owner: postgres
--

ALTER SEQUENCE crawldb.site_id_seq OWNED BY crawldb.site.id;


--
-- Name: counters; Type: TABLE; Schema: showcase; Owner: postgres
--

CREATE TABLE showcase.counters (
    counter_id integer NOT NULL,
    value integer NOT NULL
);


ALTER TABLE showcase.counters OWNER TO postgres;

--
-- Name: image id; Type: DEFAULT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.image ALTER COLUMN id SET DEFAULT nextval('crawldb.image_id_seq'::regclass);


--
-- Name: page id; Type: DEFAULT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page ALTER COLUMN id SET DEFAULT nextval('crawldb.page_id_seq'::regclass);


--
-- Name: page_data id; Type: DEFAULT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_data ALTER COLUMN id SET DEFAULT nextval('crawldb.page_data_id_seq'::regclass);


--
-- Name: site id; Type: DEFAULT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.site ALTER COLUMN id SET DEFAULT nextval('crawldb.site_id_seq'::regclass);


--
-- Data for Name: data_type; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--

COPY crawldb.data_type (code) FROM stdin;
PDF
DOC
DOCX
PPT
PPTX
\.


--
-- Data for Name: image; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--

COPY crawldb.image (id, page_id, filename, content_type, data, accessed_time) FROM stdin;
\.


--
-- Data for Name: link; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--

COPY crawldb.link (from_page, to_page) FROM stdin;
\.


--
-- Data for Name: page; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--

COPY crawldb.page (id, site_id, page_type_code, url, html_content, http_status_code, accessed_time, in_progress, html_hash) FROM stdin;
\.


--
-- Data for Name: page_data; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--

COPY crawldb.page_data (id, page_id, data_type_code, data) FROM stdin;
\.


--
-- Data for Name: page_type; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--

COPY crawldb.page_type (code) FROM stdin;
HTML
BINARY
DUPLICATE
FRONTIER
FAIL
DISALLOWED
\.


--
-- Data for Name: site; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--

COPY crawldb.site (id, domain, robots_content, sitemap_content, last_accessed_time) FROM stdin;
\.


--
-- Data for Name: counters; Type: TABLE DATA; Schema: showcase; Owner: postgres
--

COPY showcase.counters (counter_id, value) FROM stdin;
2	3000
1	1085
\.


--
-- Name: image_id_seq; Type: SEQUENCE SET; Schema: crawldb; Owner: postgres
--

SELECT pg_catalog.setval('crawldb.image_id_seq', 2431, true);


--
-- Name: page_data_id_seq; Type: SEQUENCE SET; Schema: crawldb; Owner: postgres
--

SELECT pg_catalog.setval('crawldb.page_data_id_seq', 5, true);


--
-- Name: page_id_seq; Type: SEQUENCE SET; Schema: crawldb; Owner: postgres
--

SELECT pg_catalog.setval('crawldb.page_id_seq', 48034, true);


--
-- Name: site_id_seq; Type: SEQUENCE SET; Schema: crawldb; Owner: postgres
--

SELECT pg_catalog.setval('crawldb.site_id_seq', 478, true);


--
-- Name: link _0; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.link
    ADD CONSTRAINT _0 PRIMARY KEY (from_page, to_page);


--
-- Name: data_type pk_data_type_code; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.data_type
    ADD CONSTRAINT pk_data_type_code PRIMARY KEY (code);


--
-- Name: image pk_image_id; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.image
    ADD CONSTRAINT pk_image_id PRIMARY KEY (id);


--
-- Name: page_data pk_page_data_id; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_data
    ADD CONSTRAINT pk_page_data_id PRIMARY KEY (id);


--
-- Name: page pk_page_id; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page
    ADD CONSTRAINT pk_page_id PRIMARY KEY (id);


--
-- Name: page_type pk_page_type_code; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_type
    ADD CONSTRAINT pk_page_type_code PRIMARY KEY (code);


--
-- Name: site pk_site_id; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.site
    ADD CONSTRAINT pk_site_id PRIMARY KEY (id);


--
-- Name: counters pk_counters; Type: CONSTRAINT; Schema: showcase; Owner: postgres
--

ALTER TABLE ONLY showcase.counters
    ADD CONSTRAINT pk_counters PRIMARY KEY (counter_id);


--
-- Name: idx_html_hash; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_html_hash ON crawldb.page USING btree (html_hash);


--
-- Name: idx_image_page_id; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_image_page_id ON crawldb.image USING btree (page_id);


--
-- Name: idx_link_from_page; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_link_from_page ON crawldb.link USING btree (from_page);


--
-- Name: idx_link_to_page; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_link_to_page ON crawldb.link USING btree (to_page);


--
-- Name: idx_page_data_data_type_code; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_page_data_data_type_code ON crawldb.page_data USING btree (data_type_code);


--
-- Name: idx_page_data_page_id; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_page_data_page_id ON crawldb.page_data USING btree (page_id);


--
-- Name: idx_page_page_type_code; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_page_page_type_code ON crawldb.page USING btree (page_type_code);


--
-- Name: idx_page_site_id; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_page_site_id ON crawldb.page USING btree (site_id);


--
-- Name: image fk_image_page_data; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.image
    ADD CONSTRAINT fk_image_page_data FOREIGN KEY (page_id) REFERENCES crawldb.page(id) ON DELETE RESTRICT;


--
-- Name: link fk_link_page; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.link
    ADD CONSTRAINT fk_link_page FOREIGN KEY (from_page) REFERENCES crawldb.page(id) ON DELETE RESTRICT;


--
-- Name: link fk_link_page_1; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.link
    ADD CONSTRAINT fk_link_page_1 FOREIGN KEY (to_page) REFERENCES crawldb.page(id) ON DELETE RESTRICT;


--
-- Name: page_data fk_page_data_data_type; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_data
    ADD CONSTRAINT fk_page_data_data_type FOREIGN KEY (data_type_code) REFERENCES crawldb.data_type(code) ON DELETE RESTRICT;


--
-- Name: page_data fk_page_data_page; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_data
    ADD CONSTRAINT fk_page_data_page FOREIGN KEY (page_id) REFERENCES crawldb.page(id) ON DELETE RESTRICT;


--
-- Name: page fk_page_page_type; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page
    ADD CONSTRAINT fk_page_page_type FOREIGN KEY (page_type_code) REFERENCES crawldb.page_type(code) ON DELETE RESTRICT;


--
-- Name: page fk_page_site; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page
    ADD CONSTRAINT fk_page_site FOREIGN KEY (site_id) REFERENCES crawldb.site(id) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

