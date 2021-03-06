CREATE SEQUENCE gm_pv_res_la_2018_gid_seq;

CREATE TABLE public.gm_pv_res_la_2018
(
    gid integer NOT NULL DEFAULT nextval('gm_pv_res_la_2018_gid_seq'::regclass),
    gm_code character varying(6) COLLATE pg_catalog."default",
    gm_naam character varying(60) COLLATE pg_catalog."default",
    pv_code character varying(4) COLLATE pg_catalog."default",
    pv_naam character varying(60) COLLATE pg_catalog."default",
    res_code character varying(5) COLLATE pg_catalog."default",
    res_naam character varying(60) COLLATE pg_catalog."default",
    la_code character varying(2) COLLATE pg_catalog."default",
    la_naam character varying(60) COLLATE pg_catalog."default",
    CONSTRAINT gm_pv_res_la_2018_pkey PRIMARY KEY (gid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.gm_pv_res_la_2018
    OWNER to postgres;


CREATE INDEX gm_pv_res_la_2018_pv_code_idx
    ON public.gm_pv_res_la_2018 USING btree
    (pv_code COLLATE pg_catalog."default")
    TABLESPACE pg_default;

CREATE INDEX gm_pv_res_la_2018_res_code_idx
    ON public.gm_pv_res_la_2018 USING btree
    (res_code COLLATE pg_catalog."default")
    TABLESPACE pg_default;