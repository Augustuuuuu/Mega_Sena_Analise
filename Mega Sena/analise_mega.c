#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_NUMEROS 60
#define MAX_LINHA 256
#define MAX_NUMEROS_LINHA 6

// Estrutura para armazenar número e sua frequência
typedef struct {
    int numero;
    int frequencia;
} NumeroFrequencia;

// Estrutura para armazenar contagem de pares e ímpares
typedef struct {
    int pares;
    int impares;
} ContagemParImpar;

// Função para comparar números (usada no qsort)
int compararNumeros(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

// Função para comparar frequências (usada no qsort)
int compararFrequencias(const void* a, const void* b) {
    NumeroFrequencia* nf1 = (NumeroFrequencia*)a;
    NumeroFrequencia* nf2 = (NumeroFrequencia*)b;
    
    if (nf1->frequencia != nf2->frequencia) {
        return nf2->frequencia - nf1->frequencia;
    }
    return nf1->numero - nf2->numero;
}

// Função para comparar frequências (ordem crescente)
int compararFrequenciasCrescente(const void* a, const void* b) {
    NumeroFrequencia* nf1 = (NumeroFrequencia*)a;
    NumeroFrequencia* nf2 = (NumeroFrequencia*)b;
    
    if (nf1->frequencia != nf2->frequencia) {
        return nf1->frequencia - nf2->frequencia;
    }
    return nf1->numero - nf2->numero;
}

// Função para extrair números de uma linha
int extrairNumeros(const char* linha, int* numeros) {
    int count = 0;
    char* token;
    char linha_copia[MAX_LINHA];
    char* inicio;
    
    strcpy(linha_copia, linha);
    
    // Procura pelo traço
    inicio = strchr(linha_copia, '-');
    if (!inicio) return 0;
    
    // Pula o traço e espaços
    inicio++;
    while (isspace(*inicio)) inicio++;
    
    // Divide a string pelos números
    token = strtok(inicio, ",");
    while (token != NULL && count < MAX_NUMEROS_LINHA) {
        // Remove espaços em branco
        while (isspace(*token)) token++;
        
        // Converte para número
        numeros[count++] = atoi(token);
        token = strtok(NULL, ",");
    }
    
    return count;
}

// Função para contar números pares e ímpares
ContagemParImpar contarParesImpares(NumeroFrequencia* frequencias, int total_frequencias, int quantidade) {
    ContagemParImpar contagem = {0, 0};
    int i;
    
    for (i = 0; i < quantidade && i < total_frequencias; i++) {
        if (frequencias[i].numero % 2 == 0) {
            contagem.pares++;
        } else {
            contagem.impares++;
        }
    }
    
    return contagem;
}

// Função principal de análise
void analisarNumeros(const char* arquivo, int quantidade, int tipo_ordenacao) {
    FILE* fp;
    char linha[MAX_LINHA];
    int numeros[MAX_NUMEROS * 1000];  // Array para todos os números
    int total_numeros = 0;
    NumeroFrequencia frequencias[MAX_NUMEROS];
    int total_frequencias = 0;
    int numeros_linha[MAX_NUMEROS_LINHA];
    int count;
    int i;
    int numero_atual;
    int freq_atual;
    ContagemParImpar contagem;
    
    // Abre o arquivo
    fp = fopen(arquivo, "r");
    if (fp == NULL) {
        printf("Erro ao abrir o arquivo %s\n", arquivo);
        return;
    }
    
    // Lê o arquivo linha por linha
    while (fgets(linha, sizeof(linha), fp)) {
        count = extrairNumeros(linha, numeros_linha);
        
        // Adiciona os números ao array principal
        for (i = 0; i < count; i++) {
            numeros[total_numeros++] = numeros_linha[i];
        }
    }
    
    fclose(fp);
    
    // Verifica se foram encontrados números
    if (total_numeros == 0) {
        printf("Nenhum número encontrado no arquivo.\n");
        return;
    }
    
    // Ordena os números
    qsort(numeros, total_numeros, sizeof(int), compararNumeros);
    
    // Calcula frequências
    numero_atual = numeros[0];
    freq_atual = 1;
    
    for (i = 1; i < total_numeros; i++) {
        if (numeros[i] == numero_atual) {
            freq_atual++;
        } else {
            frequencias[total_frequencias].numero = numero_atual;
            frequencias[total_frequencias].frequencia = freq_atual;
            total_frequencias++;
            
            numero_atual = numeros[i];
            freq_atual = 1;
        }
    }
    
    // Adiciona o último número
    frequencias[total_frequencias].numero = numero_atual;
    frequencias[total_frequencias].frequencia = freq_atual;
    total_frequencias++;
    
    // Ordena por frequência de acordo com o tipo escolhido
    if (tipo_ordenacao == 1) {
        qsort(frequencias, total_frequencias, sizeof(NumeroFrequencia), compararFrequencias);
        printf("\nNúmeros mais sorteados:\n");
    } else {
        qsort(frequencias, total_frequencias, sizeof(NumeroFrequencia), compararFrequenciasCrescente);
        printf("\nNúmeros menos sorteados:\n");
    }
    
    // Imprime os resultados
    for (i = 0; i < quantidade && i < total_frequencias; i++) {
        printf("Número %d: %d vezes\n", frequencias[i].numero, frequencias[i].frequencia);
    }
    
    // Conta e mostra a quantidade de números pares e ímpares
    contagem = contarParesImpares(frequencias, total_frequencias, quantidade);
    printf("\nQuantidade de números pares: %d\n", contagem.pares);
    printf("Quantidade de números ímpares: %d\n", contagem.impares);
}

void mostrarMenu() {
    printf("\n=== Menu de Análise da Mega Sena ===\n");
    printf("1. Números mais sorteados\n");
    printf("2. Números menos sorteados\n");
    printf("0. Sair\n");
    printf("Escolha uma opção: ");
}

int main() {
    char arquivo[] = "resultados.txt";
    int quantidade;
    int opcao;
    
    do {
        mostrarMenu();
        scanf("%d", &opcao);
        
        if (opcao == 0) {
            printf("Programa encerrado.\n");
            break;
        }
        
        if (opcao != 1 && opcao != 2) {
            printf("Opção inválida! Tente novamente.\n");
            continue;
        }
        
        printf("Quantos números você deseja ver? ");
        scanf("%d", &quantidade);
        
        if (quantidade < 1 || quantidade > 60) {
            printf("Por favor, insira um número entre 1 e 60.\n");
            continue;
        }
        
        analisarNumeros(arquivo, quantidade, opcao);
        printf("\nPressione Enter para continuar...");
        getchar(); // Limpa o buffer
        getchar();
        
    } while (opcao != 0);
    
    return 0;
} 