"""Reusable political worldviews. Profiles belong to governors, not countries."""
from dataclasses import dataclass


@dataclass(frozen=True)
class IdeologyProfile:
    id: str
    name: str
    description: str
    priorities: str
    tradeoffs: str
    foreign_policy: str


PROFILES = {
    "social_liberal": IdeologyProfile(
        "social_liberal", "Social-democrata",
        "Estado ativo, economia de mercado regulada e proteção social.",
        "Redução da desigualdade, saúde, educação, serviços públicos e crescimento inclusivo.",
        "Aceita maior carga tributária e dívida moderada para financiar políticas sociais; preserva responsabilidade fiscal no longo prazo.",
        "Cooperação multilateral, integração regional e diplomacia."
    ),
    "market_liberal": IdeologyProfile(
        "market_liberal", "Liberal de mercado",
        "Mercados competitivos, iniciativa privada e Estado mais enxuto.",
        "Produtividade, estabilidade monetária, simplificação tributária, investimento privado e abertura comercial.",
        "Prioriza eficiência e equilíbrio fiscal; aceita menor expansão de gastos sociais no curto prazo.",
        "Comércio aberto, alianças pragmáticas e instituições internacionais."
    ),
    "nationalist": IdeologyProfile(
        "nationalist", "Nacionalista",
        "Soberania nacional, indústria estratégica e autonomia decisória.",
        "Defesa, infraestrutura estratégica, indústria nacional, segurança energética e controle de setores críticos.",
        "Aceita protecionismo e maior gasto estatal em setores estratégicos; pondera custos de isolamento comercial.",
        "Pragmatismo soberano, dissuasão e acordos bilaterais seletivos."
    ),
    "socialist": IdeologyProfile(
        "socialist", "Socialista",
        "Planejamento público forte, redistribuição e propriedade pública em setores estratégicos.",
        "Serviços universais, redução de desigualdade, investimento público e direitos trabalhistas.",
        "Aceita impostos e intervenção econômica maiores; precisa administrar riscos de ineficiência e pressão fiscal.",
        "Solidariedade internacional, cooperação Sul-Sul e integração econômica."
    ),
    "authoritarian": IdeologyProfile(
        "authoritarian", "Autoritário desenvolvimentista",
        "Centralização do poder, ordem interna e desenvolvimento conduzido pelo Estado.",
        "Estabilidade política, infraestrutura, defesa, capacidade industrial e metas nacionais de longo prazo.",
        "Aceita restrições institucionais e liberdades civis em nome de controle; enfrenta riscos de corrupção e baixa responsabilização.",
        "Realpolitik, segurança do regime e alianças conforme interesse estratégico."
    ),
    "green": IdeologyProfile(
        "green", "Ecologista",
        "Desenvolvimento sustentável, transição energética e proteção ambiental.",
        "Energia limpa, saúde, educação, inovação verde e resiliência climática.",
        "Aceita custos de transição no curto prazo para reduzir riscos ambientais e dependência de combustíveis fósseis.",
        "Acordos climáticos, cooperação científica e diplomacia multilateral."
    ),
}


def get_profile(profile_id: str) -> IdeologyProfile:
    try:
        return PROFILES[profile_id]
    except KeyError as exc:
        raise ValueError(f"Unknown ideology profile: {profile_id}") from exc
