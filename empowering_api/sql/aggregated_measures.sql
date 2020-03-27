select
  cups,
  meter_id,
  cups,
  timestamp,
  tarifa,
  case when substring(tarifa from 1 for 1) = '2' then 'R' else 'T' end as resource,
  json_agg(json_build_object(lower(period), value, 'tipus', tipus) order by period, tipus) as measures
from (
    select
        cups.name as cups,
        c.id as meter_id,
        l.name as timestamp,
        t.name as tarifa,
        tmpl.name as period,
        coalesce(l.consum, 0) as value,
        l.tipus as tipus
    from giscedata_lectures_lectura l
        inner join giscedata_polissa_tarifa_periodes p on l.periode = p.id
        inner join giscedata_polissa_tarifa t on p.tarifa = t.id
        inner join product_product prod on p.product_id = prod.id
        inner join product_template tmpl on prod.product_tmpl_id = tmpl.id
        inner join giscedata_lectures_comptador c on l.comptador = c.id
        inner join giscedata_polissa pol on c.polissa = pol.id
        inner join giscedata_cups_ps cups on pol.cups = cups.id
    where c.id in %(ids)s

    union

    select
        cups.name as cups,
        c.id as meter_id,
        l.name as timestamp,
        t.name as tarifa,
        tmpl.name as period,
        coalesce(l.lectura, 0) as value,
        'P' as tipus
    from giscedata_lectures_potencia l
        inner join giscedata_polissa_tarifa_periodes p on l.periode = p.id
        inner join giscedata_polissa_tarifa t on p.tarifa = t.id
        inner join product_product prod on p.product_id = prod.id
        inner join product_template tmpl on prod.product_tmpl_id = tmpl.id
        inner join giscedata_lectures_comptador c on l.comptador = c.id
        inner join giscedata_polissa pol on c.polissa = pol.id
        inner join giscedata_cups_ps cups on pol.cups = cups.id
    where c.id in %(ids)s

) as foo
where timestamp >= %(date_start)s
group by cups, meter_id, timestamp, tarifa
order by meter_id, timestamp

