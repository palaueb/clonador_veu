
import argparse

def main():
    print("Aquest script permet confirmar la configuració del sistema")
    print("Si desconeixes els paràmetres, revisa el codi font o la documentació al projecte github.com/palaueb/clonador-veu\n")
    parser = argparse.ArgumentParser(description="Test de configuració del sistema")
    
#    parser.add_argument("--help", action="help", help="Mostra aquesta ajuda i surt")
    parser.add_argument("--test-cuda", action="store_true", help="Prova si CUDA està disponible")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    if args.test_cuda:
        test_cuda()

def test_cuda():
    import torch

    disponible = torch.cuda.is_available()
    if disponible:
        print("CUDA està disponible.")
        print(f"Nombre de GPUs disponibles: {torch.cuda.device_count()}")
        print(f"GPU actual: {torch.cuda.current_device()}")
        print(f"Nom de la GPU actual: {torch.cuda.get_device_name(torch.cuda.current_device())}")
        print(f"Memòria total de la GPU: {torch.cuda.get_device_properties(torch.cuda.current_device()).total_memory / (1024 ** 3):.2f} GB")
    else:
        print("CUDA no està disponible. Assegura't que tens els drivers i biblioteques necessàries instal·lades.")
        return

if __name__ == "__main__":
    main()
else:
    print("This script is not meant to be imported as a module.")
    print("Run it directly to test different options.")