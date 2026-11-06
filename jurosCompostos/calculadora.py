import math
import re
import tkinter.messagebox as caixa

import customtkinter as ctk


def calcular_juros(capital: float, taxa_mensal: float, meses: int) -> float:
    if not math.isfinite(capital) or capital < 0:
        raise ValueError("O valor inicial deve ser um número finito e não negativo.")
    if not math.isfinite(taxa_mensal) or taxa_mensal <= -100:
        raise ValueError("A taxa mensal deve ser finita e maior que -100%.")
    if meses < 0:
        raise ValueError("O prazo não pode ser negativo.")

    return capital * (1 + taxa_mensal / 100) ** meses


def formatar_reais(valor: float) -> str:
    formatado = f"{valor:,.2f}"
    formatado = formatado.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {formatado}"


def ler_decimal(texto: str, campo: str) -> float:
    normalizado = texto.strip()
    if "," in normalizado:
        if not re.fullmatch(r"[+-]?(?:\d+|\d{1,3}(?:\.\d{3})+),\d+", normalizado):
            raise ValueError(f"{campo} deve ser um número válido.")
        normalizado = normalizado.replace(".", "").replace(",", ".")

    try:
        return float(normalizado)
    except ValueError:
        raise ValueError(f"{campo} deve ser um número válido.") from None


def ler_meses(texto: str) -> int:
    try:
        return int(texto.strip())
    except ValueError:
        raise ValueError("O prazo deve ser informado em meses inteiros.") from None


def calcular() -> None:
    try:
        capital = ler_decimal(entrada_capital.get(), "O valor inicial")
        taxa = ler_decimal(entrada_taxa.get(), "A taxa mensal")
        meses = ler_meses(entrada_meses.get())
        montante = calcular_juros(capital, taxa, meses)
    except ValueError as erro:
        caixa.showerror("Dados inválidos", str(erro) or "Confira os valores digitados.")
        return
    except OverflowError:
        caixa.showerror("Resultado inválido", "O valor final é grande demais para calcular.")
        return

    juros = montante - capital
    rotulo_montante.configure(text=formatar_reais(montante))
    rotulo_juros.configure(text=f"Juros ganhos: {formatar_reais(juros)}")


def iniciar() -> None:
    global entrada_capital, entrada_taxa, entrada_meses
    global rotulo_montante, rotulo_juros

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()
    janela.title("Calculadora de Juros Compostos")
    janela.geometry("420x430")
    janela.resizable(False, False)

    ctk.CTkLabel(
        janela, text="Calculadora de Juros Compostos", font=ctk.CTkFont(size=20, weight="bold")
    ).pack(pady=(24, 18))

    formulario = ctk.CTkFrame(janela)
    formulario.pack(fill="x", padx=28)

    ctk.CTkLabel(formulario, text="Valor inicial (R$)").pack(anchor="w", padx=16, pady=(14, 4))
    entrada_capital = ctk.CTkEntry(formulario, placeholder_text="Ex.: 1000,00")
    entrada_capital.pack(fill="x", padx=16)

    ctk.CTkLabel(formulario, text="Taxa de juros mensal (%)").pack(anchor="w", padx=16, pady=(12, 4))
    entrada_taxa = ctk.CTkEntry(formulario, placeholder_text="Ex.: 1,5")
    entrada_taxa.pack(fill="x", padx=16)

    ctk.CTkLabel(formulario, text="Prazo (meses)").pack(anchor="w", padx=16, pady=(12, 4))
    entrada_meses = ctk.CTkEntry(formulario, placeholder_text="Ex.: 12")
    entrada_meses.pack(fill="x", padx=16, pady=(0, 16))

    ctk.CTkButton(janela, text="Calcular", command=calcular).pack(pady=18)

    rotulo_montante = ctk.CTkLabel(
        janela, text="Preencha os dados para ver o resultado.", font=ctk.CTkFont(size=16, weight="bold")
    )
    rotulo_montante.pack(pady=(4, 2))
    rotulo_juros = ctk.CTkLabel(janela, text="")
    rotulo_juros.pack()

    janela.mainloop()


if __name__ == "__main__":
    iniciar()
