SELECT wk_code,geom FROM public.wijk_2018_wgs
WHERE gm_code in (SELECT gm_code FROM public.gm_pv_2018 WHERE pv_code = 'PV28');
