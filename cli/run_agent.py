import argparse
import logging
import os
from dotenv import load_dotenv
from agent import Agent

def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run the agent with specified parameters.')
    parser.add_argument('--config', type=str, required=True, help='Path to the configuration file.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging.')
    return parser.parse_args()

def main():
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    args = parse_arguments()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ No se encontró la clave de API de OpenAI.")
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info('Starting agent...')
    
    try:
        agent = Agent(config_path=args.config)
        agent.run()
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        raise

if __name__ == '__main__':
    main()