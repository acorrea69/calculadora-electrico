import streamlit as st
from urllib.parse import quote

# >>> CAMBIÁ ESTE DATO POR EL TUYO <<<
# Código de país + número, sin el 0 inicial, sin espacios ni signos. Ej: 595981123456
NUMERO_WHATSAPP = "595XXXXXXXXX"

st.set_page_config(page_title="Ahorro Auto Eléctrico vs Convencional", page_icon="🔋", layout="centered")

st.title("🔋 Calculadora de Ahorro: Auto Eléctrico vs Convencional")
st.caption("Paraguay — compará cuánto podrías ahorrar por mes cambiando a un auto eléctrico, "
           "y cuánto de ese ahorro podría cubrir la cuota del auto nuevo.")

st.info("🚗 ¿Vendés autos eléctricos? Esta calculadora ayuda a tus clientes a decidirse. "
        "Al final de la página podés pedirla con la marca de tu negocio.")

st.divider()

# ---------------------------------------------------------
# 1. Uso del vehículo
# ---------------------------------------------------------
st.subheader("🚗 Uso del vehículo")
km_mensuales = st.number_input("Kilómetros que recorrés por mes", min_value=0.0, value=1500.0, step=50.0)

st.divider()

# ---------------------------------------------------------
# 2. Auto a combustión
# ---------------------------------------------------------
st.subheader("⛽ Auto a combustión")
col1, col2 = st.columns(2)
with col1:
    precio_combustible = st.number_input("Precio del combustible (Gs/litro)", min_value=0.0, value=7800.0, step=50.0)
    consumo_combustible = st.number_input("Consumo (litros cada 100 km)", min_value=0.0, value=8.0, step=0.5)
with col2:
    mantenimiento_combustion = st.number_input("Mantenimiento mensual promedio (Gs)", min_value=0.0, value=250000.0, step=10000.0,
                                                 help="Aceite, filtros, service, etc. prorrateado por mes")

st.divider()

# ---------------------------------------------------------
# 3. Auto eléctrico
# ---------------------------------------------------------
st.subheader("⚡ Auto eléctrico")
col3, col4 = st.columns(2)
with col3:
    precio_kwh = st.number_input("Precio del kWh (ANDE, Gs/kWh)", min_value=0.0, value=750.0, step=10.0)
    consumo_kwh = st.number_input("Consumo (kWh cada 100 km)", min_value=0.0, value=15.0, step=0.5)
with col4:
    mantenimiento_electrico = st.number_input("Mantenimiento mensual promedio (Gs)", min_value=0.0, value=80000.0, step=10000.0,
                                                help="Los EV no usan aceite ni tienen tantas piezas móviles")

st.divider()

# ---------------------------------------------------------
# 4. Cargador domiciliario y cuota
# ---------------------------------------------------------
st.subheader("🔌 Instalación del cargador y financiamiento")
col5, col6 = st.columns(2)
with col5:
    costo_cargador = st.number_input("Costo de instalación del cargador domiciliario (Gs)", min_value=0.0, value=6000000.0, step=100000.0)
with col6:
    cuota_auto = st.number_input("Cuota mensual estimada del auto eléctrico (Gs, opcional)", min_value=0.0, value=0.0, step=50000.0,
                                   help="Si ya tenés una cotización de financiamiento, ponela acá para ver cuánto cubre el ahorro")

st.divider()

# ---------------------------------------------------------
# Cálculos
# ---------------------------------------------------------
costo_mensual_combustible = (km_mensuales / 100) * consumo_combustible * precio_combustible
costo_mensual_electrico = (km_mensuales / 100) * consumo_kwh * precio_kwh

ahorro_energia = costo_mensual_combustible - costo_mensual_electrico
ahorro_mantenimiento = mantenimiento_combustion - mantenimiento_electrico
ahorro_mensual_total = ahorro_energia + ahorro_mantenimiento

# ---------------------------------------------------------
# Resultados
# ---------------------------------------------------------
st.header("📊 Resultados")

r1, r2 = st.columns(2)
with r1:
    st.metric("Costo combustible / mes", f"Gs {costo_mensual_combustible:,.0f}".replace(",", "."))
    st.metric("Mantenimiento combustión / mes", f"Gs {mantenimiento_combustion:,.0f}".replace(",", "."))
with r2:
    st.metric("Costo electricidad / mes", f"Gs {costo_mensual_electrico:,.0f}".replace(",", "."))
    st.metric("Mantenimiento eléctrico / mes", f"Gs {mantenimiento_electrico:,.0f}".replace(",", "."))

st.markdown("### 💰 Ahorro mensual total")
st.metric("Ahorro mensual (energía + mantenimiento)", f"Gs {ahorro_mensual_total:,.0f}".replace(",", "."),
          delta=f"Energía: Gs {ahorro_energia:,.0f} | Mantenimiento: Gs {ahorro_mantenimiento:,.0f}".replace(",", "."))

if ahorro_mensual_total > 0:
    meses_recuperar_cargador = costo_cargador / ahorro_mensual_total
    st.info(f"🔌 Con este ahorro, el costo del cargador domiciliario (Gs {costo_cargador:,.0f}".replace(",", ".") +
            f") se recupera en aproximadamente **{meses_recuperar_cargador:.1f} meses**.")

    if cuota_auto > 0:
        st.markdown("### 🚘 Uso del ahorro para la cuota del auto")
        if ahorro_mensual_total >= cuota_auto:
            sobrante = ahorro_mensual_total - cuota_auto
            st.success(f"✅ El ahorro mensual **cubre completamente** la cuota estimada de Gs {cuota_auto:,.0f}"
                        .replace(",", ".") + f", y todavía quedan Gs {sobrante:,.0f} extra por mes.".replace(",", "."))
        else:
            falta = cuota_auto - ahorro_mensual_total
            porcentaje = (ahorro_mensual_total / cuota_auto) * 100
            st.warning(f"⚠️ El ahorro mensual cubre el **{porcentaje:.0f}%** de la cuota estimada. "
                        f"Faltarían Gs {falta:,.0f} por mes de otra fuente.".replace(",", "."))
else:
    st.error("⚠️ Con estos valores, el auto eléctrico no genera ahorro mensual respecto al de combustión. "
             "Revisá el precio del kWh o el consumo eléctrico ingresado.")

st.divider()

# ---------------------------------------------------------
# Ahorro acumulado a 12 y 24 meses
# ---------------------------------------------------------
st.subheader("📈 Ahorro acumulado")
ahorro_12 = ahorro_mensual_total * 12
ahorro_24 = ahorro_mensual_total * 24
ahorro_12_neto = ahorro_12 - costo_cargador
ahorro_24_neto = ahorro_24 - costo_cargador

c1, c2 = st.columns(2)
with c1:
    st.metric("Ahorro bruto a 12 meses", f"Gs {ahorro_12:,.0f}".replace(",", "."))
    st.metric("Ahorro neto a 12 meses (descontando cargador)", f"Gs {ahorro_12_neto:,.0f}".replace(",", "."))
with c2:
    st.metric("Ahorro bruto a 24 meses", f"Gs {ahorro_24:,.0f}".replace(",", "."))
    st.metric("Ahorro neto a 24 meses (descontando cargador)", f"Gs {ahorro_24_neto:,.0f}".replace(",", "."))

st.caption("Nota: esta calculadora usa valores promedio ingresados por el usuario y no considera variaciones "
           "en el precio del combustible, tarifas escalonadas de ANDE, depreciación del vehículo ni costos de seguro.")

# ---------------------------------------------------------
# Contacto
# ---------------------------------------------------------
st.divider()
st.subheader("¿Querés esta calculadora con la marca de tu negocio?")
st.write("La personalizo con tu logo, tus colores y tus modelos de autos, y la usan tus clientes desde tu web o tu WhatsApp.")
texto_wa = quote("Hola, vi la calculadora de auto eléctrico y quiero saber más")
st.link_button("💬 Escribime por WhatsApp", f"https://wa.me/{NUMERO_WHATSAPP}?text={texto_wa}")
