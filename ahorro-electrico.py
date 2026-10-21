import streamlit as st
from urllib.parse import quote

# >>> CAMBIÁ ESTE DATO POR EL TUYO <<<
# Código de país + número, sin el 0 inicial, sin espacios ni signos. Ej: 595981123456
NUMERO_WHATSAPP = "595985870756"

def gs(valor):
    return f"Gs {valor:,.0f}".replace(",", ".")

st.set_page_config(page_title="Ahorro Auto Eléctrico vs Convencional", page_icon="🔋", layout="centered")

st.title("🔋 Calculadora de Ahorro: Auto Eléctrico vs Convencional")
st.caption("Si estás pensando en cambiar de auto, "
           "compará cuánto podrías ahorrar por mes cambiando a un auto eléctrico, "
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
    precio_combustible = st.number_input("Precio del combustible (Gs/litro)", min_value=0.0, value=7500.0, step=50.0)
    st.caption(f"= {gs(precio_combustible)} por litro")
    consumo_combustible = st.number_input("Consumo (litros cada 100 km)", min_value=0.0, value=8.0, step=0.5)
with col2:
    mantenimiento_combustion = st.number_input("Mantenimiento mensual promedio (Gs)", min_value=0.0, value=150000.0, step=10000.0,
                                                 help="Aceite, filtros, service, etc. prorrateado por mes")
    st.caption(f"= {gs(mantenimiento_combustion)} por mes")

st.divider()

# ---------------------------------------------------------
# 3. Auto eléctrico
# ---------------------------------------------------------
st.subheader("⚡ Auto eléctrico")
col3, col4 = st.columns(2)
with col3:
    precio_kwh = st.number_input("Precio del kWh (ANDE, Gs/kWh)", min_value=0.0, value=500.0, step=10.0)
    st.caption(f"= {gs(precio_kwh)} por kWh")
    consumo_kwh = st.number_input("Consumo (kWh cada 100 km)", min_value=0.0, value=15.0, step=0.5)
with col4:
    mantenimiento_electrico = st.number_input("Mantenimiento mensual promedio (Gs)", min_value=0.0, value=50000.0, step=10000.0,
                                                help="Los EV no usan aceite ni tienen tantas piezas móviles")
    st.caption(f"= {gs(mantenimiento_electrico)} por mes")

st.divider()

# ---------------------------------------------------------
# 4. Cuota del auto
# ---------------------------------------------------------
st.subheader("🚘 Financiamiento del auto eléctrico")
cuota_auto = st.number_input("Cuota mensual estimada del auto eléctrico (Gs)", min_value=0.0, value=1500000.0, step=50000.0,
                             help="Poné la cuota de la cotización de financiamiento para ver qué porcentaje se paga solo con el ahorro")
st.caption(f"= {gs(cuota_auto)} por mes")

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
    if cuota_auto > 0:
        porcentaje = (ahorro_mensual_total / cuota_auto) * 100
        st.markdown("### 🚘 ¿Cuánto de la cuota se paga solo?")
        st.markdown(
            f"""
            <div style="text-align:center; padding: 0.5rem 0 0.25rem 0;">
                <div style="font-size:4.5rem; font-weight:800; line-height:1.1;">{porcentaje:.0f}%</div>
                <div style="font-size:1.15rem;">de la cuota del auto se paga solo con lo que dejás de gastar
                en combustible y mantenimiento</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(porcentaje / 100, 1.0))
        if ahorro_mensual_total >= cuota_auto:
            sobrante = ahorro_mensual_total - cuota_auto
            st.success(f"✅ El ahorro mensual cubre completamente la cuota de {gs(cuota_auto)} "
                       f"y todavía sobran {gs(sobrante)} por mes.")
        else:
            falta = cuota_auto - ahorro_mensual_total
            st.info(f"El ahorro mensual de {gs(ahorro_mensual_total)} cubre parte de la cuota de {gs(cuota_auto)}. "
                    f"Lo que faltaría pagar cada mes: {gs(falta)}.")
    else:
        st.info("Ingresá la cuota mensual estimada del auto para ver qué porcentaje se paga solo con el ahorro.")
else:
    st.error("⚠️ Con estos valores, el auto eléctrico no genera ahorro mensual respecto al de combustión. "
             "Revisá el precio del kWh o el consumo eléctrico ingresado.")

st.divider()

st.caption("Nota: esta calculadora usa valores promedio ingresados por el usuario y no considera variaciones "
           "en el precio del combustible, tarifas escalonadas de ANDE, depreciación del vehículo ni costos de seguro.")

# ---------------------------------------------------------
# Contacto
# ---------------------------------------------------------
st.divider()
st.markdown("<h3 style='text-align:center;'>¿Querés esta calculadora con la marca de tu negocio?</h3>",
            unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>La personalizo con tu logo, tus colores y tus modelos de autos, "
            "y la usan tus clientes desde tu web o tu WhatsApp.</p>", unsafe_allow_html=True)
texto_wa = quote("Hola, vi la calculadora de auto eléctrico y quiero saber más")
_, centro, _ = st.columns([1, 2, 1])
with centro:
    st.link_button("💬 Escribime por WhatsApp", f"https://wa.me/{NUMERO_WHATSAPP}?text={texto_wa}",
                   use_container_width=True)
