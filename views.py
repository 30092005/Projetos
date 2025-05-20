from django.shortcuts import render, redirect
import datetime
import holidays
from django.db.models import Q
import calendar
from .forms import FeriadoPersonalizadoForm
from .models import FeriadoPersonalizado
from datetime import date

# View para criar feriado personalizado
def criar_feriado(request):
    if request.method == "POST":
        form = FeriadoPersonalizadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_feriados")
    else:
        form = FeriadoPersonalizadoForm()

    return render(request, "timeline/criar_feriados.html", {"form": form})

# View para listar feriados personalizados
def listar_feriados(request):
    feriados = FeriadoPersonalizado.objects.all()
    return render(request, "timeline/listar_feriados.html", {"feriados": feriados})


# Lista de estados e seus municípios
MUNICIPIOS = {
    "AC - Acre": ["Rio Branco", "Cruzeiro do Sul", "Sena Madureira"],
    "AL - Alagoas": ["Maceió", "Arapiraca", "Palmeira dos Índios"],
    "AP - Amapá": ["Macapá", "Santana", "Laranjal do Jari"],
    "AM - Amazonas": ["Manaus", "Parintins", "Itacoatiara"],
    "BA - Bahia": ["Salvador", "Feira de Santana", "Vitória da Conquista"],
    "CE - Ceará": ["Fortaleza", "Caucaia", "Sobral"],
    "DF - Distrito Federal": ["Brasília"],
    "ES - Espírito Santo": ["Vitória", "Vila Velha", "Serra"],
    "GO - Goiás": ["Goiânia", "Aparecida de Goiânia", "Anápolis"],
    "MA - Maranhão": ["São Luís", "Imperatriz", "Caxias"],
    "MT - Mato Grosso": ["Cuiabá", "Várzea Grande", "Rondonópolis"],
    "MS - Mato Grosso do Sul": ["Campo Grande", "Dourados", "Três Lagoas"],
    "MG - Minas Gerais": ["Belo Horizonte", "Uberlândia", "Contagem"],
    "PR - Paraná": ["Curitiba", "Londrina", "Maringá"],
    "PB - Paraíba": ["João Pessoa", "Campina Grande", "Patos"],
    "PE - Pernambuco": ["Recife", "Olinda", "Jaboatão dos Guararapes"],
    "PI - Piauí": ["Teresina", "Parnaíba", "Picos"],
    "RJ - Rio de Janeiro": ["Rio de Janeiro", "Niterói", "Campos dos Goytacazes"],
    "RN - Rio Grande do Norte": ["Natal", "Mossoró", "Parnamirim"],
    "RS - Rio Grande do Sul": ["Porto Alegre", "Caxias do Sul", "Pelotas"],
    "RO - Rondônia": ["Porto Velho", "Ji-Paraná", "Ariquemes"],
    "RR - Roraima": ["Boa Vista", "Rorainópolis", "Caracaraí"],
    "SC - Santa Catarina": ["Florianópolis", "Joinville", "Blumenau"],
    "SE - Sergipe": ["Aracaju", "Nossa Senhora do Socorro", "Lagarto"],
    "SP - São Paulo": ["São Paulo", "Campinas", "Santos"],
    "TO - Tocantins": ["Palmas", "Araguaína", "Gurupi"]
}

# Tradução dos nomes dos feriados vindos da biblioteca holidays
TRADUCAO_FERIADOS = {
    "New Year's Day": "Confraternização Universal",
    "Carnival": "Carnaval",
    "Carnival Monday": "Segunda-feira de Carnaval",
    "Carnival Tuesday": "Terça-feira de Carnaval",
    "Ash Wednesday": "Quarta-feira de Cinzas",
    "Good Friday": "Sexta-feira Santa",
    "Easter Sunday": "Domingo de Páscoa",
    "Tiradentes' Day": "Dia de Tiradentes",
    "Labour Day": "Dia do Trabalhador",
    "Corpus Christi": "Corpus Christi",
    "Independence Day": "Dia da Independência",
    "Our Lady of Aparecida": "Nossa Senhora Aparecida",
    "All Souls' Day": "Dia de Finados",
    "All Saints' Day": "Dia de Todos os Santos",
    "Republic Day": "Proclamação da República",
    "Christmas Day": "Natal",
    "Black Awareness Day": "Dia da Consciência Negra",
    "Flag Day": "Dia da Bandeira",
    "Armed Forces Day": "Dia das Forças Armadas",
    "Father's Day": "Dia dos Pais",
    "Mother's Day": "Dia das Mães",
    "Valentine's Day": "Dia dos Namorados",
    "Children's Day": "Dia das Crianças",
    "Teacher's Day": "Dia do Professor",
    "Saint John's Day": "São João",
    "Saint Peter and Saint Paul's Day": "São Pedro e São Paulo",
    "Saint Joseph's Day": "São José",
    "Saint George's Day": "São Jorge",
    "Holy Saturday": "Sábado de Aleluia",
    "Palm Sunday": "Domingo de Ramos",
    "Worker's Day": "Dia do Trabalhador"
}
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}


def traduzir_feriado(nome_en):
    return TRADUCAO_FERIADOS.get(nome_en, nome_en)

# Função principal para cálculo de prazos
def calcular_prazo(data_inicial, dias_corridos, estado_sigla, municipio=None):
    feriados_nacionais = holidays.Brazil(language='pt')
    feriados_estaduais = holidays.Brazil(subdiv=estado_sigla, language='pt')

    try:
        feriados_municipais = holidays.Brazil(subdiv=estado_sigla, city=municipio, language='pt') if municipio else {}
    except Exception:
        feriados_municipais = {}

    # Feriados personalizados do banco de dados
    feriados_custom = FeriadoPersonalizado.objects.filter(data__year=data_inicial.year)
    if estado_sigla:
        feriados_custom = feriados_custom.filter(Q(estado=estado_sigla) | Q(estado__isnull=True))
    if municipio:
        feriados_custom = feriados_custom.filter(Q(municipio=municipio) | Q(municipio__isnull=True))
    datas_custom = {feriado.data: feriado for feriado in feriados_custom}

    dias_validos = []
    todos_os_dias = []
    data = data_inicial

    while len(dias_validos) < dias_corridos:
        tipo = "útil"
        feriado_nome = ""
        tipo_feriado = ""

        if data in feriados_nacionais:
            tipo = "feriado"
            feriado_nome = traduzir_feriado(feriados_nacionais.get(data))
            tipo_feriado = "Feriado Nacional"
        elif data in feriados_estaduais:
            tipo = "feriado"
            feriado_nome = traduzir_feriado(feriados_estaduais.get(data))
            tipo_feriado = "Feriado Estadual"
        elif data in feriados_municipais:
            tipo = "feriado"
            feriado_nome = traduzir_feriado(feriados_municipais.get(data))
            tipo_feriado = "Feriado Municipal"
        elif data in datas_custom:
            tipo = "feriado"
            feriado_nome = datas_custom[data].nome
            tipo_feriado = f"Feriado Personalizado ({datas_custom[data].tipo})"
        elif data.weekday() >= 5:
            tipo = "fim_de_semana"

        if tipo == "útil":
            dias_validos.append(data)

        todos_os_dias.append({
            "data": data,
            "tipo": tipo,
            "feriado_nome": feriado_nome,
            "tipo_feriado": tipo_feriado
        })

        data += datetime.timedelta(days=1)

    return dias_validos, todos_os_dias

# View principal (home)
def home(request):
    resultado = None
    dias_validos = []
    todos_os_dias = []
    erro = None
    estado_completo = ""
    municipio = ""

    if request.method == "POST":
        data_str = request.POST.get("data_inicial")
        estado_completo = request.POST.get("estado")
        municipio = request.POST.get("municipio") or None

        try:
            dias_corridos = int(request.POST.get("dias_corridos"))
            data_inicial = datetime.datetime.strptime(data_str, "%Y-%m-%d").date()
            estado_sigla = estado_completo.split(" - ")[0]
        except (ValueError, TypeError, AttributeError):
            erro = "Data, número de dias ou estado inválido."
            return render(request, "timeline/home.html", {
                "erro": erro,
                "municipios": MUNICIPIOS
            })

        try:
            dias_validos, todos_os_dias = calcular_prazo(data_inicial, dias_corridos, estado_sigla, municipio)
            resultado = dias_validos[-1] if dias_validos else None
        except Exception as e:
            erro = f"Erro ao calcular prazo: {str(e)}"

    return render(request, "timeline/home.html", {
        "resultado": resultado,
        "dias_validos": dias_validos,
        "todos_os_dias": todos_os_dias,
        "municipios": MUNICIPIOS,
        "erro": erro,
        "estado_selecionado": estado_completo,
        "municipio_selecionado": municipio
    })

from datetime import date, datetime
def agenda(request):
    now = datetime.now()
    today = now.date()

    # Trata parâmetros da URL
    try:
        year = int(request.GET.get('year', today.year))
    except (ValueError, TypeError):
        year = today.year

    try:
        month = int(request.GET.get('month', today.month))
    except (ValueError, TypeError):
        month = today.month

    meses_pt = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    current_month_name = meses_pt[month - 1]

    weekdays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

    br_holidays = holidays.Brazil(years=year)
    br_holidays_traduzidos = {
        k: TRADUCAO_FERIADOS.get(v, v) for k, v in br_holidays.items()
    }

    _, last_day = calendar.monthrange(year, month)
    all_days = [date(year, month, day) for day in range(1, last_day + 1)]

    calendar_weeks = []
    week = []

    for d in all_days:
        is_today = (d == today)
        is_holiday = d in br_holidays_traduzidos
        holiday_name = br_holidays_traduzidos.get(d) if is_holiday else None

        day_info = {
            'date': d,
            'is_today': is_today,
            'is_holiday': is_holiday,
            'holiday_name': holiday_name,
        }

        # Preenche dias anteriores ao domingo no início da semana
        if len(week) == 0 and d.weekday() != 6:  # domingo == 6
            week.extend([None] * ((d.weekday() + 1) % 7))

        week.append(day_info)

        if len(week) == 7:
            calendar_weeks.append(week)
            week = []

    if week:
        while len(week) < 7:
            week.append(None)
        calendar_weeks.append(week)

    previous_month = 12 if month == 1 else month - 1
    previous_year = year - 1 if month == 1 else year
    next_month = 1 if month == 12 else month + 1
    next_year = year + 1 if month == 12 else year

    context = {
        'calendar_weeks': calendar_weeks,
        'current_year': year,
        'current_month': month,
        'current_month_name': current_month_name,
        'weekdays': weekdays,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': today,
        'current_time': now.strftime('%H:%M'),
    }

    return render(request, 'timeline/agenda.html', context)