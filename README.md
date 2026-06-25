# Resumen de Costos — Mensajeria y Voz

Vista ejecutiva interactiva del gasto en comunicaciones de BaldeCash (Enero–Junio 2026).

**Live:** [miguelbaldecash.github.io/Resumen_Costo_Mensajeria](https://miguelbaldecash.github.io/Resumen_Costo_Mensajeria/)

## Contenido

### Tabla 1: WhatsApp por area de negocio
Mensajes WA (Blip + Botmaker + Voximplant) agrupados por:
- Cobranza en mora
- Cobranza preventiva
- Retargeting / Campanas
- Preadmision
- Entrega / Ops
- Otros / Sin clasificar

Con totales y costo estimado USD por mes.

### Tabla 2: Otros canales
- Llamadas Voximplant PSTN
- Llamadas Kontactus
- Email GoHighLevel (cobranza)
- Email Mailgun (transaccional)
- SMS Labs Mobile

### Drill-down interactivo
Click en cualquier area para ver:
- **Atribucion:** Msgs y costo por mes, desglosable por plataforma, tipo Meta (MKT/UTIL/AUTH), fee Meta vs fee plataforma
- **Intensidad:** Distribucion de msgs por telefono (cuantos phones reciben 1 msg, 2-3, 21+, etc.)
- **Plantillas:** Buscador de plantillas con volumen y costo, filtrable por mes

### Toggle proyeccion
Opcion de proyectar el mes parcial (junio 23 dias) al mes completo (30 dias).

## Datos
- Periodo: Enero–Junio 23, 2026
- Fuentes: Blip, Botmaker, Voximplant, GoHighLevel, Mailgun, Labs Mobile, Kontactus
- Factura Blip mayo: INV/2026/00752 ($12,509.92)
- Junio: sin factura, costo estimado con blended rate mayo ($0.0827/msg)

## Archivos
| Archivo | Descripcion |
|---|---|
| `index.html` | Dashboard interactivo |
| `template_data.js` | 408 plantillas con volumen por mes |
| `template_totals.js` | Totales por area y tipo Meta |
| `phone_inline.js` | Numeros destino por mes |
| `template_phones.js` | Plantilla x telefono x mes |
| `template_contents.js` | Contenido de plantillas WA |
