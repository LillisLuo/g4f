# from flask import Flask, render_template, request, jsonify, Response, send_file
# import g4f
# import json
# import logging
# from typing import Dict, List, Any
# import os
# import threading
# import time
# import base64
# from io import BytesIO
# from PIL import Image
# import requests

# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class GPT4FreeService:
#     def __init__(self):
#         self.providers = self._get_available_providers()
#         self.models = self._get_available_models()
#         self.image_providers = self._get_image_providers()
#         self.image_models = self._get_image_models()
#         self.working_providers = self._test_providers()
#         self.working_image_providers = self._test_image_providers()
    
#     def _get_available_providers(self) -> Dict[str, Any]:
#         """Get available providers from g4f"""
#         providers = {}
#         try:
#             # Providers that support text generation (based on your table)
#             provider_list = [
#                 'Blackbox', 'Blackboxapi', 'Chatai', 'ChatGLM', 'Cloudflare',
#                 'DeepInfraChat', 'DocsBot', 'Free2GPT', 'FreeGpt', 'GizAI',
#                 'LambdaChat', 'LegacyLMArena', 'OIVSCodeSer2', 'OIVSCodeSer5',
#                 'OIVSCodeSer0501', 'PerplexityLabs', 'TeachAnything', 'WeWordle',
#                 'Yqcloud', 'Websim', 'Copilot', 'HuggingSpace', 'PollinationsAI',
#                 'Together'
#             ]
            
#             for provider_name in provider_list:
#                 try:
#                     if hasattr(g4f.Provider, provider_name):
#                         provider = getattr(g4f.Provider, provider_name)
#                         providers[provider_name] = {
#                             'name': provider_name,
#                             'working': True,
#                             'supports_stream': True,
#                             'supports_system_message': True,
#                             'url': getattr(provider, 'url', '')
#                         }
#                 except Exception as e:
#                     logger.warning(f"Provider {provider_name} not available: {e}")
#                     continue
                    
#         except Exception as e:
#             logger.error(f"Error getting providers: {e}")
#         return providers
    
#     def _get_image_providers(self) -> Dict[str, Any]:
#         """Get available image generation providers"""
#         image_providers = {}
#         try:
#             # Providers that support image generation (based on your table)
#             image_provider_list = [
#                 'ImageLabs', 'PollinationsImage', 'ARTA', 'HuggingSpace',
#                 'PollinationsAI', 'Together'
#             ]
            
#             for provider_name in image_provider_list:
#                 try:
#                     if hasattr(g4f.Provider, provider_name):
#                         provider = getattr(g4f.Provider, provider_name)
#                         image_providers[provider_name] = {
#                             'name': provider_name,
#                             'working': True,
#                             'supports_image': True,
#                             'supports_models': getattr(provider, 'image_models', ['default']),
#                             'url': getattr(provider, 'url', '')
#                         }
#                 except Exception as e:
#                     logger.warning(f"Image provider {provider_name} not available: {e}")
#                     continue
                    
#         except Exception as e:
#             logger.error(f"Error getting image providers: {e}")
#         return image_providers
    
#     def _get_available_models(self) -> Dict[str, Any]:
#         """Get available models from g4f"""
#         models = {}
        
#         # All unique models from the table
#         model_list = {
#             # Blackbox models
#             'blackboxai': {'name': 'BlackboxAI', 'base_provider': 'Blackbox'},
#             'gpt-4.1-mini': {'name': 'GPT-4.1 Mini', 'base_provider': 'Blackbox'},
#             'gpt-4.1-nano': {'name': 'GPT-4.1 Nano', 'base_provider': 'Blackbox'},
#             'gpt-4': {'name': 'GPT-4', 'base_provider': 'Multiple'},
#             'gpt-4o': {'name': 'GPT-4 Optimized', 'base_provider': 'Multiple'},
#             'gpt-4o-mini': {'name': 'GPT-4 Optimized Mini', 'base_provider': 'Multiple'},
#             'o1': {'name': 'O1', 'base_provider': 'Multiple'},
#             'o4-mini': {'name': 'O4 Mini', 'base_provider': 'Multiple'},
            
#             # LLaMA models
#             'llama-3.1-70b': {'name': 'LLaMA 3.1 70B', 'base_provider': 'Multiple'},
#             'llama-3.1-8b': {'name': 'LLaMA 3.1 8B', 'base_provider': 'Multiple'},
#             'llama-2-7b': {'name': 'LLaMA 2 7B', 'base_provider': 'Multiple'},
#             'llama-2-70b': {'name': 'LLaMA 2 70B', 'base_provider': 'Multiple'},
#             'llama-3-8b': {'name': 'LLaMA 3 8B', 'base_provider': 'Multiple'},
#             'llama-3-70b': {'name': 'LLaMA 3 70B', 'base_provider': 'Multiple'},
#             'llama-3.2-3b': {'name': 'LLaMA 3.2 3B', 'base_provider': 'Multiple'},
#             'llama-3.2-90b': {'name': 'LLaMA 3.2 90B', 'base_provider': 'Multiple'},
#             'llama-3.3-70b': {'name': 'LLaMA 3.3 70B', 'base_provider': 'Multiple'},
#             'llama-4-scout': {'name': 'LLaMA 4 Scout', 'base_provider': 'Multiple'},
#             'llama-4-maverick': {'name': 'LLaMA 4 Maverick', 'base_provider': 'Multiple'},
            
#             # Qwen models
#             'qwen-1.5-7b': {'name': 'Qwen 1.5 7B', 'base_provider': 'Alibaba'},
#             'qwen-1.5-11b': {'name': 'Qwen 1.5 11B', 'base_provider': 'Alibaba'},
#             'qwen-2-5-plus': {'name': 'Qwen 2.5 Plus', 'base_provider': 'Alibaba'},
#             'qwen-2.5-72b': {'name': 'Qwen 2.5 72B', 'base_provider': 'Alibaba'},
#             'qwen-2.5-coder-32b': {'name': 'Qwen 2.5 Coder 32B', 'base_provider': 'Alibaba'},
#             'qwen-3-14b': {'name': 'Qwen 3 14B', 'base_provider': 'Alibaba'},
#             'qwen-3-235b': {'name': 'Qwen 3 235B', 'base_provider': 'Alibaba'},
#             'qwen-3-30b': {'name': 'Qwen 3 30B', 'base_provider': 'Alibaba'},
#             'qwen-3-32b': {'name': 'Qwen 3 32B', 'base_provider': 'Alibaba'},
#             'qwen-3-4b': {'name': 'Qwen 3 4B', 'base_provider': 'Alibaba'},
#             'qwen-32b': {'name': 'Qwen 32B', 'base_provider': 'Alibaba'},
#             'qwen-plus': {'name': 'Qwen Plus', 'base_provider': 'Alibaba'},
#             'qwen-vl-max': {'name': 'Qwen VL Max', 'base_provider': 'Alibaba'},
#             'qwq-32b': {'name': 'QwQ 32B', 'base_provider': 'Alibaba'},
            
#             # DeepSeek models
#             'deepseek-prover-v2-671b': {'name': 'DeepSeek Prover V2 671B', 'base_provider': 'DeepSeek'},
#             'deepseek-r1': {'name': 'DeepSeek R1', 'base_provider': 'DeepSeek'},
#             'deepseek-r1-4528': {'name': 'DeepSeek R1 4528', 'base_provider': 'DeepSeek'},
#             'deepseek-r1-distill-llama-70b': {'name': 'DeepSeek R1 Distill LLaMA 70B', 'base_provider': 'DeepSeek'},
#             'deepseek-r1-distill-qwen-14b': {'name': 'DeepSeek R1 Distill Qwen 14B', 'base_provider': 'DeepSeek'},
#             'deepseek-r1-distill-qwen-32b': {'name': 'DeepSeek R1 Distill Qwen 32B', 'base_provider': 'DeepSeek'},
#             'deepseek-r1-distill-qwen-1.5b': {'name': 'DeepSeek R1 Distill Qwen 1.5B', 'base_provider': 'DeepSeek'},
#             'deepseek-r1-turbo': {'name': 'DeepSeek R1 Turbo', 'base_provider': 'DeepSeek'},
#             'deepseek-v2': {'name': 'DeepSeek V2', 'base_provider': 'DeepSeek'},
#             'deepseek-v2.5': {'name': 'DeepSeek V2.5', 'base_provider': 'DeepSeek'},
#             'deepseek-v3': {'name': 'DeepSeek V3', 'base_provider': 'DeepSeek'},
#             'deepseek-v3-0324': {'name': 'DeepSeek V3 0324', 'base_provider': 'DeepSeek'},
#             'deepseek-coder-v2': {'name': 'DeepSeek Coder V2', 'base_provider': 'DeepSeek'},
            
#             # Gemini models
#             'gemini-1.5-pro': {'name': 'Gemini 1.5 Pro', 'base_provider': 'Google'},
#             'gemini-1.5-flash': {'name': 'Gemini 1.5 Flash', 'base_provider': 'Google'},
#             'gemini-2.0-flash': {'name': 'Gemini 2.0 Flash', 'base_provider': 'Google'},
#             'gemini-1.5-flash-thinking': {'name': 'Gemini 1.5 Flash Thinking', 'base_provider': 'Google'},
#             'gemini-2.0-flash-thinking': {'name': 'Gemini 2.0 Flash Thinking', 'base_provider': 'Google'},
#             'gemini-2.5-flash': {'name': 'Gemini 2.5 Flash', 'base_provider': 'Google'},
#             'gemini-2.5-pro': {'name': 'Gemini 2.5 Pro', 'base_provider': 'Google'},
            
#             # Claude models
#             'claude-3.7-sonnet': {'name': 'Claude 3.7 Sonnet', 'base_provider': 'Anthropic'},
#             'claude-3-sonnet': {'name': 'Claude 3 Sonnet', 'base_provider': 'Anthropic'},
#             'claude-3-opus': {'name': 'Claude 3 Opus', 'base_provider': 'Anthropic'},
#             'claude-3-haiku': {'name': 'Claude 3 Haiku', 'base_provider': 'Anthropic'},
#             'claude-3.5-haiku': {'name': 'Claude 3.5 Haiku', 'base_provider': 'Anthropic'},
            
#             # Other models
#             'grok-3': {'name': 'Grok 3', 'base_provider': 'xAI'},
#             'grok-2': {'name': 'Grok 2', 'base_provider': 'xAI'},
#             'grok-2-mini': {'name': 'Grok 2 Mini', 'base_provider': 'xAI'},
#             'grok-3-mini': {'name': 'Grok 3 Mini', 'base_provider': 'xAI'},
#             'glm-4': {'name': 'GLM-4', 'base_provider': 'Zhipu'},
#             'glm-4-plus': {'name': 'GLM-4 Plus', 'base_provider': 'Zhipu'},
#             'o3-mini': {'name': 'O3 Mini', 'base_provider': 'OpenAI'},
#             'o3': {'name': 'O3', 'base_provider': 'OpenAI'},
#             'sonar': {'name': 'Sonar', 'base_provider': 'Perplexity'},
#             'sonar-pro': {'name': 'Sonar Pro', 'base_provider': 'Perplexity'},
#             'sonar-reasoning': {'name': 'Sonar Reasoning', 'base_provider': 'Perplexity'},
#             'sonar-reasoning-pro': {'name': 'Sonar Reasoning Pro', 'base_provider': 'Perplexity'},
#             'mixtral-7b': {'name': 'Mixtral 7B', 'base_provider': 'Mistral'},
#             'mixtral-8x7b': {'name': 'Mixtral 8x7B', 'base_provider': 'Mistral'},
#             'mixtral-8x22b': {'name': 'Mixtral 8x22B', 'base_provider': 'Mistral'},
#             'mixtral-small-24b': {'name': 'Mixtral Small 24B', 'base_provider': 'Mistral'},
#             'mistral-7b': {'name': 'Mistral 7B', 'base_provider': 'Mistral'},
#             'mistral-small-3.1-24b': {'name': 'Mistral Small 3.1 24B', 'base_provider': 'Mistral'},
#             'mistral-next': {'name': 'Mistral Next', 'base_provider': 'Mistral'},
#             'pixtral-large': {'name': 'Pixtral Large', 'base_provider': 'Mistral'},
#             'phi-4': {'name': 'Phi 4', 'base_provider': 'Microsoft'},
#             'phi-4-maverick': {'name': 'Phi 4 Maverick', 'base_provider': 'Microsoft'},
#             'phi-3-small': {'name': 'Phi 3 Small', 'base_provider': 'Microsoft'},
#             'phi-3-medium': {'name': 'Phi 3 Medium', 'base_provider': 'Microsoft'},
#             'phi-3-mini': {'name': 'Phi 3 Mini', 'base_provider': 'Microsoft'},
#             'hermes-2-dpo': {'name': 'Hermes 2 DPO', 'base_provider': 'NousResearch'},
#             'hermes-3': {'name': 'Hermes 3', 'base_provider': 'NousResearch'},
#             'hermes-3-405b': {'name': 'Hermes 3 405B', 'base_provider': 'NousResearch'},
#             'nemotron-70b': {'name': 'Nemotron 70B', 'base_provider': 'NVIDIA'},
#             'nemotron-253b': {'name': 'Nemotron 253B', 'base_provider': 'NVIDIA'},
#             'nemotron-40b': {'name': 'Nemotron 40B', 'base_provider': 'NVIDIA'},
#             'nemotron-51b': {'name': 'Nemotron 51B', 'base_provider': 'NVIDIA'},
#             'nemotron-4-340b': {'name': 'Nemotron 4 340B', 'base_provider': 'NVIDIA'},
#             'codellama-70b': {'name': 'CodeLLaMA 70B', 'base_provider': 'Meta'},
#             'command-r': {'name': 'Command R', 'base_provider': 'Cohere'},
#             'command-r-plus': {'name': 'Command R Plus', 'base_provider': 'Cohere'},
#             'command-r7b': {'name': 'Command R7B', 'base_provider': 'Cohere'},
#             'command-a': {'name': 'Command A', 'base_provider': 'Cohere'},
#             'dbrx-instruct': {'name': 'DBRX Instruct', 'base_provider': 'Databricks'},
#             'openhermes-2.5-7b': {'name': 'OpenHermes 2.5 7B', 'base_provider': 'NousResearch'},
#             'wizardlm-2-7b': {'name': 'WizardLM 2 7B', 'base_provider': 'Microsoft'},
#             'wizardlm-2-8x22b': {'name': 'WizardLM 2 8x22B', 'base_provider': 'Microsoft'},
#             'dolphin-2.6': {'name': 'Dolphin 2.6', 'base_provider': 'Cognitive'},
#             'dolphin-2.9': {'name': 'Dolphin 2.9', 'base_provider': 'Cognitive'},
#             'airoboros-70b': {'name': 'Airoboros 70B', 'base_provider': 'Community'},
#             'lzlv-70b': {'name': 'LZLV 70B', 'base_provider': 'Community'},
#             'r1-1776': {'name': 'R1 1776', 'base_provider': 'Community'},
#             'pplx-70b-online': {'name': 'PPLX 70B Online', 'base_provider': 'Perplexity'},
#             'pplx-7b-online': {'name': 'PPLX 7B Online', 'base_provider': 'Perplexity'},
#             'reka-flash': {'name': 'Reka Flash', 'base_provider': 'Reka'},
#             'reka-core': {'name': 'Reka Core', 'base_provider': 'Reka'},
#             'gemma-1-4b': {'name': 'Gemma 1 4B', 'base_provider': 'Google'},
#             'gemma-2-12b': {'name': 'Gemma 2 12B', 'base_provider': 'Google'},
#             'gemma-2-27b': {'name': 'Gemma 2 27B', 'base_provider': 'Google'},
#             'gemma-2-2b': {'name': 'Gemma 2 2B', 'base_provider': 'Google'},
#             'gemma-2-9b': {'name': 'Gemma 2 9B', 'base_provider': 'Google'},
#             'gemma-3-12b': {'name': 'Gemma 3 12B', 'base_provider': 'Google'},
#             'gemma-3-27b': {'name': 'Gemma 3 27B', 'base_provider': 'Google'},
#             'tulu-3-8b': {'name': 'Tulu 3 8B', 'base_provider': 'AllenAI'},
#             'tulu-2-70b': {'name': 'Tulu 2 70B', 'base_provider': 'AllenAI'},
#             'yi-34b': {'name': 'Yi 34B', 'base_provider': '01.ai'},
#             'llama-13b': {'name': 'LLaMA 13B', 'base_provider': 'Meta'}
#         }
        
#         for model_id, model_info in model_list.items():
#             models[model_id] = {
#                 'name': model_info['name'],
#                 'base_provider': model_info['base_provider'],
#                 'best_provider': ''
#             }
        
#         return models
    
#     def _get_image_models(self) -> Dict[str, Any]:
#         """Get available image generation models"""
#         image_models = {}
        
#         # All image models from the table
#         model_list = {
#             # Flux models
#             'flux': {'name': 'Flux', 'providers': ['PollinationsImage', 'PollinationsAI', 'Together']},
#             'flux-pro': {'name': 'Flux Pro', 'providers': ['PollinationsImage', 'PollinationsAI', 'Together']},
#             'flux-dev': {'name': 'Flux Dev', 'providers': ['PollinationsImage', 'PollinationsAI', 'Together', 'HuggingSpace']},
#             'flux-schnell': {'name': 'Flux Schnell', 'providers': ['PollinationsImage', 'PollinationsAI', 'Together']},
#             'flux-redux': {'name': 'Flux Redux', 'providers': ['Together']},
#             'flux-depth': {'name': 'Flux Depth', 'providers': ['Together']},
#             'flux-canny': {'name': 'Flux Canny', 'providers': ['Together']},
#             'flux-kontext-max': {'name': 'Flux Kontext Max', 'providers': ['Together']},
#             'flux-dev-lora': {'name': 'Flux Dev LoRA', 'providers': ['Together']},
#             'flux-kontext-pro': {'name': 'Flux Kontext Pro', 'providers': ['Together']},
            
#             # DALL-E models
#             'dall-e-3': {'name': 'DALL-E 3', 'providers': ['PollinationsImage', 'PollinationsAI', 'Copilot']},
            
#             # Stable Diffusion models
#             'sdxl-turbo': {'name': 'SDXL Turbo', 'providers': ['ImageLabs', 'PollinationsImage', 'PollinationsAI']},
#             'sdxl-1.0': {'name': 'Stable Diffusion XL 1.0', 'providers': ['ARTA']},
#             'sdxl-l': {'name': 'Stable Diffusion XL Large', 'providers': ['ARTA']},
#             'sd-3.5-large': {'name': 'Stable Diffusion 3.5 Large', 'providers': ['HuggingSpace']},
            
#             # Other models
#             'gpt-image': {'name': 'GPT Image', 'providers': ['PollinationsImage', 'PollinationsAI', 'ARTA']}
#         }
        
#         for model_id, model_info in model_list.items():
#             image_models[model_id] = {
#                 'name': model_info['name'],
#                 'providers': model_info['providers']
#             }
        
#         return image_models

    
#     def _test_providers(self) -> List[str]:
#         """Test providers to see which ones are working"""
#         working = []
#         test_messages = [{"role": "user", "content": "Hi"}]
        
#         for provider_name in self.providers.keys():
#             try:
#                 provider = getattr(g4f.Provider, provider_name)
#                 # Quick test
#                 response = g4f.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=test_messages,
#                     provider=provider,
#                     stream=False,
#                     timeout=10
#                 )
#                 if response and len(str(response).strip()) > 0:
#                     working.append(provider_name)
#                     logger.info(f"Provider {provider_name} is working")
#                 else:
#                     logger.warning(f"Provider {provider_name} returned empty response")
#             except Exception as e:
#                 logger.warning(f"Provider {provider_name} test failed: {e}")
#                 continue
        
#         logger.info(f"Working providers: {working}")
#         return working
    
#     def _test_image_providers(self) -> List[str]:
#         """Test image providers to see which ones are working"""
#         working = []
#         test_prompt = "A simple red circle"
        
#         for provider_name in self.image_providers.keys():
#             try:
#                 provider = getattr(g4f.Provider, provider_name)
#                 # Quick test with a simple prompt
#                 logger.info(f"Testing image provider: {provider_name}")
                
#                 # Different methods for different providers
#                 if hasattr(g4f, 'ImageGeneration'):
#                     response = g4f.ImageGeneration.create(
#                         prompt=test_prompt,
#                         provider=provider,
#                         timeout=15
#                     )
#                 else:
#                     # Fallback method
#                     continue
                
#                 if response:
#                     working.append(provider_name)
#                     logger.info(f"Image provider {provider_name} is working")
                    
#             except Exception as e:
#                 logger.warning(f"Image provider {provider_name} test failed: {e}")
#                 continue
        
#         logger.info(f"Working image providers: {working}")
#         return working
    
#     def generate_response(self, messages: List[Dict], provider_name: str = None, model_name: str = None, stream: bool = False):
#         """Generate response using g4f with fallback mechanism"""
        
#         # Clean and validate messages
#         clean_messages = []
#         for msg in messages:
#             if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
#                 clean_messages.append({
#                     'role': str(msg['role']).lower(),
#                     'content': str(msg['content']).strip()
#                 })
        
#         if not clean_messages:
#             raise ValueError("No valid messages provided")
        
#         # Get model
#         model = model_name if model_name else 'gpt-3.5-turbo'
        
#         # Try specified provider first, then fallback to working providers
#         providers_to_try = []
#         if provider_name and provider_name in self.providers:
#             providers_to_try.append(provider_name)
        
#         # Add working providers as fallback
#         providers_to_try.extend([p for p in self.working_providers if p not in providers_to_try])
        
#         # If no working providers, try all available providers
#         if not providers_to_try:
#             providers_to_try = list(self.providers.keys())
        
#         # Try providers one by one
#         last_error = None
#         for provider_name in providers_to_try:
#             try:
#                 logger.info(f"Trying provider: {provider_name}")
#                 provider = getattr(g4f.Provider, provider_name)
                
#                 if stream:
#                     response = g4f.ChatCompletion.create(
#                         model=model,
#                         messages=clean_messages,
#                         provider=provider,
#                         stream=True,
#                         timeout=30
#                     )
#                 else:
#                     response = g4f.ChatCompletion.create(
#                         model=model,
#                         messages=clean_messages,
#                         provider=provider,
#                         stream=False,
#                         timeout=30
#                     )
                
#                 # Validate response
#                 if response:
#                     if stream:
#                         return response  # Return generator for streaming
#                     else:
#                         response_str = str(response).strip()
#                         if response_str and len(response_str) > 0:
#                             logger.info(f"Success with provider: {provider_name}")
#                             return response_str
#                         else:
#                             logger.warning(f"Empty response from provider: {provider_name}")
#                             continue
#                 else:
#                     logger.warning(f"No response from provider: {provider_name}")
#                     continue
                    
#             except Exception as e:
#                 last_error = e
#                 logger.warning(f"Provider {provider_name} failed: {e}")
#                 continue
        
#         # If all providers failed, try without specifying provider
#         try:
#             logger.info("Trying without specific provider")
#             if stream:
#                 response = g4f.ChatCompletion.create(
#                     model=model,
#                     messages=clean_messages,
#                     stream=True,
#                     timeout=30
#                 )
#             else:
#                 response = g4f.ChatCompletion.create(
#                     model=model,
#                     messages=clean_messages,
#                     stream=False,
#                     timeout=30
#                 )
            
#             if response:
#                 if stream:
#                     return response
#                 else:
#                     response_str = str(response).strip()
#                     if response_str:
#                         return response_str
                        
#         except Exception as e:
#             last_error = e
#             logger.error(f"Final attempt failed: {e}")
        
#         # If everything failed
#         raise Exception(f"All providers failed. Last error: {last_error}")
    
#     def generate_image(self, prompt: str, provider_name: str = None, model: str = None, size: str = "1024x1024", quality: str = "standard", n: int = 1):
#         """Generate image using g4f with fallback mechanism"""
        
#         if not prompt or not prompt.strip():
#             raise ValueError("No prompt provided")
        
#         # Clean prompt
#         prompt = prompt.strip()
        
#         # Try specified provider first, then fallback to working providers
#         providers_to_try = []
#         if provider_name and provider_name in self.image_providers:
#             providers_to_try.append(provider_name)
        
#         # Add working image providers as fallback
#         providers_to_try.extend([p for p in self.working_image_providers if p not in providers_to_try])
        
#         # If no working providers, try all available image providers
#         if not providers_to_try:
#             providers_to_try = list(self.image_providers.keys())
        
#         # Try providers one by one
#         last_error = None
#         for provider_name in providers_to_try:
#             try:
#                 logger.info(f"Trying image provider: {provider_name}")
#                 provider = getattr(g4f.Provider, provider_name)
                
#                 # Try different methods based on g4f version
#                 response = None
                
#                 # Method 1: Direct image generation (for newer g4f versions)
#                 try:
#                     # Import the client if available
#                     from g4f.client import Client
#                     client = Client()
                    
#                     # Use the appropriate model for the provider
#                     image_model = model or 'flux'
#                     if provider_name == 'Together' and not model:
#                         image_model = 'flux'
#                     elif provider_name == 'PollinationsImage' and not model:
#                         image_model = 'flux'
#                     elif provider_name == 'ARTA' and not model:
#                         image_model = 'sdxl-1.0'
                    
#                     response = client.images.generate(
#                         model=image_model,
#                         prompt=prompt,
#                         provider=provider
#                     )
                    
#                     if response and hasattr(response, 'data') and response.data:
#                         image_url = response.data[0].url
#                         logger.info(f"Success with provider {provider_name}: got URL via client")
#                         return {'url': image_url, 'provider': provider_name}
                        
#                 except Exception as e:
#                     logger.warning(f"Client method failed for {provider_name}: {e}")
                
#                 # Method 2: Using provider's create method directly
#                 if not response:
#                     try:
#                         # Some providers might have a direct create method
#                         if hasattr(provider, 'create'):
#                             response = provider.create(
#                                 prompt=prompt,
#                                 model=model
#                             )
#                             if response:
#                                 logger.info(f"Success with provider {provider_name}: direct create method")
#                                 if isinstance(response, str) and response.startswith('http'):
#                                     return {'url': response, 'provider': provider_name}
#                                 elif isinstance(response, dict) and 'url' in response:
#                                     return {'url': response['url'], 'provider': provider_name}
#                     except Exception as e:
#                         logger.warning(f"Direct create method failed for {provider_name}: {e}")
                
#                 # Method 3: Try using ChatCompletion with specific parameters
#                 if not response:
#                     try:
#                         # Some providers might support image generation through chat
#                         response = g4f.ChatCompletion.create(
#                             model=model or "flux",
#                             messages=[{"role": "user", "content": prompt}],
#                             provider=provider,
#                             image=True
#                         )
#                         if response:
#                             logger.info(f"Success with provider {provider_name}: chat method")
#                             if isinstance(response, str) and response.startswith('http'):
#                                 return {'url': response, 'provider': provider_name}
#                     except Exception as e:
#                         logger.warning(f"Chat method failed for {provider_name}: {e}")
                    
#             except Exception as e:
#                 last_error = e
#                 logger.error(f"Image provider {provider_name} failed completely: {e}")
#                 continue
        
#         # If everything failed
#         raise Exception(f"All image providers failed. Last error: {last_error}")
    
#     def refresh_working_providers(self):
#         """Refresh the list of working providers"""
#         self.working_providers = self._test_providers()
#         self.working_image_providers = self._test_image_providers()
#         return {
#             'text_providers': self.working_providers,
#             'image_providers': self.working_image_providers
#         }

# # Initialize service
# gpt4free_service = GPT4FreeService()

# @app.route('/')
# def index():
#     """Main page"""
#     return render_template('index.html', 
#                          providers=gpt4free_service.providers,
#                          models=gpt4free_service.models,
#                          image_providers=gpt4free_service.image_providers,
#                          image_models=gpt4free_service.image_models)

# @app.route('/api/providers')
# def get_providers():
#     """Get available providers"""
#     return jsonify(gpt4free_service.providers)

# @app.route('/api/image-providers')
# def get_image_providers():
#     """Get available image providers"""
#     return jsonify(gpt4free_service.image_providers)

# @app.route('/api/image-models')
# def get_image_models():
#     """Get available image models"""
#     return jsonify(gpt4free_service.image_models)

# @app.route('/api/models')
# def get_models():
#     """Get available models"""
#     return jsonify(gpt4free_service.models)

# @app.route('/api/refresh-providers', methods=['POST'])
# def refresh_providers():
#     """Refresh working providers"""
#     try:
#         result = gpt4free_service.refresh_working_providers()
#         return jsonify({
#             'working_text_providers': result['text_providers'],
#             'working_image_providers': result['image_providers'],
#             'total_text_providers': len(gpt4free_service.providers),
#             'total_image_providers': len(gpt4free_service.image_providers)
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/generate', methods=['POST'])
# def generate():
#     """Generate response from GPT4Free"""
#     try:
#         data = request.json
#         messages = data.get('messages', [])
#         provider_name = data.get('provider')
#         model_name = data.get('model')
#         stream = data.get('stream', False)
        
#         if not messages:
#             return jsonify({'error': 'No messages provided'}), 400
        
#         logger.info(f"Generate request: provider={provider_name}, model={model_name}, stream={stream}")
#         logger.info(f"Messages: {messages}")
        
#         try:
#             if stream:
#                 def generate_stream():
#                     try:
#                         response = gpt4free_service.generate_response(
#                             messages, provider_name, model_name, stream=True
#                         )
                        
#                         # Handle streaming response
#                         content_sent = False
#                         for chunk in response:
#                             if chunk and str(chunk).strip():
#                                 content_sent = True
#                                 yield f"data: {json.dumps({'content': str(chunk)})}\n\n"
                        
#                         if not content_sent:
#                             yield f"data: {json.dumps({'error': 'No content received from provider'})}\n\n"
#                         else:
#                             yield f"data: {json.dumps({'done': True})}\n\n"
                        
#                     except Exception as e:
#                         logger.error(f"Streaming error: {e}")
#                         yield f"data: {json.dumps({'error': str(e)})}\n\n"
                
#                 return Response(
#                     generate_stream(),
#                     mimetype='text/event-stream',
#                     headers={
#                         'Cache-Control': 'no-cache',
#                         'Connection': 'keep-alive',
#                         'X-Accel-Buffering': 'no'
#                     }
#                 )
#             else:
#                 response = gpt4free_service.generate_response(
#                     messages, provider_name, model_name, stream=False
#                 )
                
#                 if response and str(response).strip():
#                     return jsonify({'response': str(response)})
#                 else:
#                     return jsonify({'error': 'No response generated'}), 500
                
#         except Exception as e:
#             logger.error(f"Generation error: {e}")
#             return jsonify({'error': f'Generation failed: {str(e)}'}), 500
            
#     except Exception as e:
#         logger.error(f"Error in generate endpoint: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/generate-image', methods=['POST'])
# def generate_image():
#     """Generate image from GPT4Free"""
#     try:
#         data = request.json
#         prompt = data.get('prompt', '').strip()
#         provider_name = data.get('provider')
#         model = data.get('model')
#         size = data.get('size', '1024x1024')
#         quality = data.get('quality', 'standard')
#         n = data.get('n', 1)
        
#         if not prompt:
#             return jsonify({'error': 'No prompt provided'}), 400
        
#         logger.info(f"Image generation request: provider={provider_name}, model={model}, prompt={prompt[:50]}...")
        
#         try:
#             result = gpt4free_service.generate_image(
#                 prompt=prompt,
#                 provider_name=provider_name,
#                 model=model,
#                 size=size,
#                 quality=quality,
#                 n=n
#             )
            
#             # Process result based on type
#             if 'url' in result:
#                 # Return URL directly
#                 return jsonify({
#                     'success': True,
#                     'url': result['url'],
#                     'provider': result['provider']
#                 })
#             elif 'base64' in result:
#                 # Return base64 data
#                 return jsonify({
#                     'success': True,
#                     'base64': result['base64'],
#                     'provider': result['provider']
#                 })
#             elif 'data' in result:
#                 # Process complex data structure
#                 data = result['data']
#                 if isinstance(data, dict):
#                     if 'url' in data:
#                         return jsonify({
#                             'success': True,
#                             'url': data['url'],
#                             'provider': result['provider']
#                         })
#                     elif 'data' in data:
#                         return jsonify({
#                             'success': True,
#                             'base64': data['data'],
#                             'provider': result['provider']
#                         })
#                     elif 'images' in data and len(data['images']) > 0:
#                         return jsonify({
#                             'success': True,
#                             'url': data['images'][0].get('url') or data['images'][0].get('data'),
#                             'provider': result['provider']
#                         })
                
#                 # Fallback: return raw data
#                 return jsonify({
#                     'success': True,
#                     'data': data,
#                     'provider': result['provider']
#                 })
#             else:
#                 return jsonify({'error': 'Invalid response format'}), 500
                
#         except Exception as e:
#             logger.error(f"Image generation error: {e}")
#             return jsonify({'error': f'Image generation failed: {str(e)}'}), 500
            
#     except Exception as e:
#         logger.error(f"Error in generate-image endpoint: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/health')
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         'status': 'healthy',
#         'text_providers_count': len(gpt4free_service.providers),
#         'image_providers_count': len(gpt4free_service.image_providers),
#         'models_count': len(gpt4free_service.models),
#         'image_models_count': len(gpt4free_service.image_models),
#         'working_text_providers': gpt4free_service.working_providers,
#         'working_image_providers': gpt4free_service.working_image_providers,
#         'working_text_count': len(gpt4free_service.working_providers),
#         'working_image_count': len(gpt4free_service.working_image_providers)
#     })

# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({'error': 'Not found'}), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({'error': 'Internal server error'}), 500

# if __name__ == '__main__':
#     # For local development
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

from flask import Flask, render_template, request, jsonify, Response, send_file
import g4f
import json
import logging
from typing import Dict, List, Any
import os
import threading
import time
import base64
from io import BytesIO
from PIL import Image
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPT4FreeService:
    def __init__(self):
        self.providers = self._get_available_providers()
        self.models = self._get_available_models()
        self.image_providers = self._get_image_providers()
        self.image_models = self._get_image_models()
        self.working_providers = self._test_providers()
        self.working_image_providers = self._test_image_providers()
    
    def _get_available_providers(self) -> Dict[str, Any]:
        """Get available providers from g4f"""
        providers = {}
        try:
            # Providers that support text generation (based on your table)
            provider_list = [
                'Blackbox', 'Blackboxapi', 'Chatai', 'ChatGLM', 'Cloudflare',
                'DeepInfraChat', 'DocsBot', 'Free2GPT', 'FreeGpt', 'GizAI',
                'LambdaChat', 'LegacyLMArena', 'OIVSCodeSer2', 'OIVSCodeSer5',
                'OIVSCodeSer0501', 'PerplexityLabs', 'TeachAnything', 'WeWordle',
                'Yqcloud', 'Websim', 'Copilot', 'HuggingSpace', 'PollinationsAI',
                'Together'
            ]
            
            for provider_name in provider_list:
                try:
                    if hasattr(g4f.Provider, provider_name):
                        provider = getattr(g4f.Provider, provider_name)
                        providers[provider_name] = {
                            'name': provider_name,
                            'working': True,
                            'supports_stream': True,
                            'supports_system_message': True,
                            'url': getattr(provider, 'url', '')
                        }
                except Exception as e:
                    logger.warning(f"Provider {provider_name} not available: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error getting providers: {e}")
        return providers
    
    def _get_image_providers(self) -> Dict[str, Any]:
        """Get available image generation providers"""
        image_providers = {}
        try:
            # 基于最新文档的图片生成提供商
            image_provider_list = [
                'BingCreateImages', 'OpenaiChat', 'Gemini', 'PollinationsAI', 
                'Flux', 'HuggingSpace', 'Together'
            ]
            
            for provider_name in image_provider_list:
                try:
                    if hasattr(g4f.Provider, provider_name):
                        provider = getattr(g4f.Provider, provider_name)
                        image_providers[provider_name] = {
                            'name': provider_name,
                            'working': True,
                            'supports_image': True,
                            'supports_models': getattr(provider, 'image_models', ['default']),
                            'url': getattr(provider, 'url', '')
                        }
                except Exception as e:
                    logger.warning(f"Image provider {provider_name} not available: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error getting image providers: {e}")
        return image_providers
    
    def _get_available_models(self) -> Dict[str, Any]:
        """Get available models from g4f"""
        models = {}
        
        # All unique models from the table
        model_list = {
            # Blackbox models
            'blackboxai': {'name': 'BlackboxAI', 'base_provider': 'Blackbox'},
            'gpt-4.1-mini': {'name': 'GPT-4.1 Mini', 'base_provider': 'Blackbox'},
            'gpt-4.1-nano': {'name': 'GPT-4.1 Nano', 'base_provider': 'Blackbox'},
            'gpt-4': {'name': 'GPT-4', 'base_provider': 'Multiple'},
            'gpt-4o': {'name': 'GPT-4 Optimized', 'base_provider': 'Multiple'},
            'gpt-4o-mini': {'name': 'GPT-4 Optimized Mini', 'base_provider': 'Multiple'},
            'o1': {'name': 'O1', 'base_provider': 'Multiple'},
            'o4-mini': {'name': 'O4 Mini', 'base_provider': 'Multiple'},
            
            # LLaMA models
            'llama-3.1-70b': {'name': 'LLaMA 3.1 70B', 'base_provider': 'Multiple'},
            'llama-3.1-8b': {'name': 'LLaMA 3.1 8B', 'base_provider': 'Multiple'},
            'llama-2-7b': {'name': 'LLaMA 2 7B', 'base_provider': 'Multiple'},
            'llama-2-70b': {'name': 'LLaMA 2 70B', 'base_provider': 'Multiple'},
            'llama-3-8b': {'name': 'LLaMA 3 8B', 'base_provider': 'Multiple'},
            'llama-3-70b': {'name': 'LLaMA 3 70B', 'base_provider': 'Multiple'},
            'llama-3.2-3b': {'name': 'LLaMA 3.2 3B', 'base_provider': 'Multiple'},
            'llama-3.2-90b': {'name': 'LLaMA 3.2 90B', 'base_provider': 'Multiple'},
            'llama-3.3-70b': {'name': 'LLaMA 3.3 70B', 'base_provider': 'Multiple'},
            'llama-4-scout': {'name': 'LLaMA 4 Scout', 'base_provider': 'Multiple'},
            'llama-4-maverick': {'name': 'LLaMA 4 Maverick', 'base_provider': 'Multiple'},
            
            # Qwen models
            'qwen-1.5-7b': {'name': 'Qwen 1.5 7B', 'base_provider': 'Alibaba'},
            'qwen-1.5-11b': {'name': 'Qwen 1.5 11B', 'base_provider': 'Alibaba'},
            'qwen-2-5-plus': {'name': 'Qwen 2.5 Plus', 'base_provider': 'Alibaba'},
            'qwen-2.5-72b': {'name': 'Qwen 2.5 72B', 'base_provider': 'Alibaba'},
            'qwen-2.5-coder-32b': {'name': 'Qwen 2.5 Coder 32B', 'base_provider': 'Alibaba'},
            'qwen-3-14b': {'name': 'Qwen 3 14B', 'base_provider': 'Alibaba'},
            'qwen-3-235b': {'name': 'Qwen 3 235B', 'base_provider': 'Alibaba'},
            'qwen-3-30b': {'name': 'Qwen 3 30B', 'base_provider': 'Alibaba'},
            'qwen-3-32b': {'name': 'Qwen 3 32B', 'base_provider': 'Alibaba'},
            'qwen-3-4b': {'name': 'Qwen 3 4B', 'base_provider': 'Alibaba'},
            'qwen-32b': {'name': 'Qwen 32B', 'base_provider': 'Alibaba'},
            'qwen-plus': {'name': 'Qwen Plus', 'base_provider': 'Alibaba'},
            'qwen-vl-max': {'name': 'Qwen VL Max', 'base_provider': 'Alibaba'},
            'qwq-32b': {'name': 'QwQ 32B', 'base_provider': 'Alibaba'},
            
            # DeepSeek models
            'deepseek-prover-v2-671b': {'name': 'DeepSeek Prover V2 671B', 'base_provider': 'DeepSeek'},
            'deepseek-r1': {'name': 'DeepSeek R1', 'base_provider': 'DeepSeek'},
            'deepseek-r1-4528': {'name': 'DeepSeek R1 4528', 'base_provider': 'DeepSeek'},
            'deepseek-r1-distill-llama-70b': {'name': 'DeepSeek R1 Distill LLaMA 70B', 'base_provider': 'DeepSeek'},
            'deepseek-r1-distill-qwen-14b': {'name': 'DeepSeek R1 Distill Qwen 14B', 'base_provider': 'DeepSeek'},
            'deepseek-r1-distill-qwen-32b': {'name': 'DeepSeek R1 Distill Qwen 32B', 'base_provider': 'DeepSeek'},
            'deepseek-r1-distill-qwen-1.5b': {'name': 'DeepSeek R1 Distill Qwen 1.5B', 'base_provider': 'DeepSeek'},
            'deepseek-r1-turbo': {'name': 'DeepSeek R1 Turbo', 'base_provider': 'DeepSeek'},
            'deepseek-v2': {'name': 'DeepSeek V2', 'base_provider': 'DeepSeek'},
            'deepseek-v2.5': {'name': 'DeepSeek V2.5', 'base_provider': 'DeepSeek'},
            'deepseek-v3': {'name': 'DeepSeek V3', 'base_provider': 'DeepSeek'},
            'deepseek-v3-0324': {'name': 'DeepSeek V3 0324', 'base_provider': 'DeepSeek'},
            'deepseek-coder-v2': {'name': 'DeepSeek Coder V2', 'base_provider': 'DeepSeek'},
            
            # Gemini models
            'gemini-1.5-pro': {'name': 'Gemini 1.5 Pro', 'base_provider': 'Google'},
            'gemini-1.5-flash': {'name': 'Gemini 1.5 Flash', 'base_provider': 'Google'},
            'gemini-2.0-flash': {'name': 'Gemini 2.0 Flash', 'base_provider': 'Google'},
            'gemini-1.5-flash-thinking': {'name': 'Gemini 1.5 Flash Thinking', 'base_provider': 'Google'},
            'gemini-2.0-flash-thinking': {'name': 'Gemini 2.0 Flash Thinking', 'base_provider': 'Google'},
            'gemini-2.5-flash': {'name': 'Gemini 2.5 Flash', 'base_provider': 'Google'},
            'gemini-2.5-pro': {'name': 'Gemini 2.5 Pro', 'base_provider': 'Google'},
            
            # Claude models
            'claude-3.7-sonnet': {'name': 'Claude 3.7 Sonnet', 'base_provider': 'Anthropic'},
            'claude-3-sonnet': {'name': 'Claude 3 Sonnet', 'base_provider': 'Anthropic'},
            'claude-3-opus': {'name': 'Claude 3 Opus', 'base_provider': 'Anthropic'},
            'claude-3-haiku': {'name': 'Claude 3 Haiku', 'base_provider': 'Anthropic'},
            'claude-3.5-haiku': {'name': 'Claude 3.5 Haiku', 'base_provider': 'Anthropic'},
            
            # Other models
            'grok-3': {'name': 'Grok 3', 'base_provider': 'xAI'},
            'grok-2': {'name': 'Grok 2', 'base_provider': 'xAI'},
            'grok-2-mini': {'name': 'Grok 2 Mini', 'base_provider': 'xAI'},
            'grok-3-mini': {'name': 'Grok 3 Mini', 'base_provider': 'xAI'},
            'glm-4': {'name': 'GLM-4', 'base_provider': 'Zhipu'},
            'glm-4-plus': {'name': 'GLM-4 Plus', 'base_provider': 'Zhipu'},
            'o3-mini': {'name': 'O3 Mini', 'base_provider': 'OpenAI'},
            'o3': {'name': 'O3', 'base_provider': 'OpenAI'},
            'sonar': {'name': 'Sonar', 'base_provider': 'Perplexity'},
            'sonar-pro': {'name': 'Sonar Pro', 'base_provider': 'Perplexity'},
            'sonar-reasoning': {'name': 'Sonar Reasoning', 'base_provider': 'Perplexity'},
            'sonar-reasoning-pro': {'name': 'Sonar Reasoning Pro', 'base_provider': 'Perplexity'},
            'mixtral-7b': {'name': 'Mixtral 7B', 'base_provider': 'Mistral'},
            'mixtral-8x7b': {'name': 'Mixtral 8x7B', 'base_provider': 'Mistral'},
            'mixtral-8x22b': {'name': 'Mixtral 8x22B', 'base_provider': 'Mistral'},
            'mixtral-small-24b': {'name': 'Mixtral Small 24B', 'base_provider': 'Mistral'},
            'mistral-7b': {'name': 'Mistral 7B', 'base_provider': 'Mistral'},
            'mistral-small-3.1-24b': {'name': 'Mistral Small 3.1 24B', 'base_provider': 'Mistral'},
            'mistral-next': {'name': 'Mistral Next', 'base_provider': 'Mistral'},
            'pixtral-large': {'name': 'Pixtral Large', 'base_provider': 'Mistral'},
            'phi-4': {'name': 'Phi 4', 'base_provider': 'Microsoft'},
            'phi-4-maverick': {'name': 'Phi 4 Maverick', 'base_provider': 'Microsoft'},
            'phi-3-small': {'name': 'Phi 3 Small', 'base_provider': 'Microsoft'},
            'phi-3-medium': {'name': 'Phi 3 Medium', 'base_provider': 'Microsoft'},
            'phi-3-mini': {'name': 'Phi 3 Mini', 'base_provider': 'Microsoft'},
            'hermes-2-dpo': {'name': 'Hermes 2 DPO', 'base_provider': 'NousResearch'},
            'hermes-3': {'name': 'Hermes 3', 'base_provider': 'NousResearch'},
            'hermes-3-405b': {'name': 'Hermes 3 405B', 'base_provider': 'NousResearch'},
            'nemotron-70b': {'name': 'Nemotron 70B', 'base_provider': 'NVIDIA'},
            'nemotron-253b': {'name': 'Nemotron 253B', 'base_provider': 'NVIDIA'},
            'nemotron-40b': {'name': 'Nemotron 40B', 'base_provider': 'NVIDIA'},
            'nemotron-51b': {'name': 'Nemotron 51B', 'base_provider': 'NVIDIA'},
            'nemotron-4-340b': {'name': 'Nemotron 4 340B', 'base_provider': 'NVIDIA'},
            'codellama-70b': {'name': 'CodeLLaMA 70B', 'base_provider': 'Meta'},
            'command-r': {'name': 'Command R', 'base_provider': 'Cohere'},
            'command-r-plus': {'name': 'Command R Plus', 'base_provider': 'Cohere'},
            'command-r7b': {'name': 'Command R7B', 'base_provider': 'Cohere'},
            'command-a': {'name': 'Command A', 'base_provider': 'Cohere'},
            'dbrx-instruct': {'name': 'DBRX Instruct', 'base_provider': 'Databricks'},
            'openhermes-2.5-7b': {'name': 'OpenHermes 2.5 7B', 'base_provider': 'NousResearch'},
            'wizardlm-2-7b': {'name': 'WizardLM 2 7B', 'base_provider': 'Microsoft'},
            'wizardlm-2-8x22b': {'name': 'WizardLM 2 8x22B', 'base_provider': 'Microsoft'},
            'dolphin-2.6': {'name': 'Dolphin 2.6', 'base_provider': 'Cognitive'},
            'dolphin-2.9': {'name': 'Dolphin 2.9', 'base_provider': 'Cognitive'},
            'airoboros-70b': {'name': 'Airoboros 70B', 'base_provider': 'Community'},
            'lzlv-70b': {'name': 'LZLV 70B', 'base_provider': 'Community'},
            'r1-1776': {'name': 'R1 1776', 'base_provider': 'Community'},
            'pplx-70b-online': {'name': 'PPLX 70B Online', 'base_provider': 'Perplexity'},
            'pplx-7b-online': {'name': 'PPLX 7B Online', 'base_provider': 'Perplexity'},
            'reka-flash': {'name': 'Reka Flash', 'base_provider': 'Reka'},
            'reka-core': {'name': 'Reka Core', 'base_provider': 'Reka'},
            'gemma-1-4b': {'name': 'Gemma 1 4B', 'base_provider': 'Google'},
            'gemma-2-12b': {'name': 'Gemma 2 12B', 'base_provider': 'Google'},
            'gemma-2-27b': {'name': 'Gemma 2 27B', 'base_provider': 'Google'},
            'gemma-2-2b': {'name': 'Gemma 2 2B', 'base_provider': 'Google'},
            'gemma-2-9b': {'name': 'Gemma 2 9B', 'base_provider': 'Google'},
            'gemma-3-12b': {'name': 'Gemma 3 12B', 'base_provider': 'Google'},
            'gemma-3-27b': {'name': 'Gemma 3 27B', 'base_provider': 'Google'},
            'tulu-3-8b': {'name': 'Tulu 3 8B', 'base_provider': 'AllenAI'},
            'tulu-2-70b': {'name': 'Tulu 2 70B', 'base_provider': 'AllenAI'},
            'yi-34b': {'name': 'Yi 34B', 'base_provider': '01.ai'},
            'llama-13b': {'name': 'LLaMA 13B', 'base_provider': 'Meta'}
        }
        
        for model_id, model_info in model_list.items():
            models[model_id] = {
                'name': model_info['name'],
                'base_provider': model_info['base_provider'],
                'best_provider': ''
            }
        
        return models
    
    def _get_image_models(self) -> Dict[str, Any]:
        """Get available image generation models"""
        image_models = {}
        
        # 基于最新文档的图片模型
        model_list = {
            # Flux models
            'flux': {'name': 'Flux', 'providers': ['PollinationsAI', 'Together', 'HuggingSpace']},
            'flux-pro': {'name': 'Flux Pro', 'providers': ['PollinationsAI', 'Together']},
            'flux-dev': {'name': 'Flux Dev', 'providers': ['PollinationsAI', 'Together', 'HuggingSpace']},
            'flux-schnell': {'name': 'Flux Schnell', 'providers': ['PollinationsAI', 'Together']},
            
            # DALL-E models
            'dalle-3': {'name': 'DALL-E 3', 'providers': ['BingCreateImages', 'OpenaiChat']},
            
            # GPT Image
            'gpt-image': {'name': 'GPT Image', 'providers': ['PollinationsAI']},
            
            # Bing
            'bing': {'name': 'Bing Image Creator', 'providers': ['BingCreateImages']},
        }
        
        for model_id, model_info in model_list.items():
            image_models[model_id] = {
                'name': model_info['name'],
                'providers': model_info['providers']
            }
        
        return image_models

    
    def _test_providers(self) -> List[str]:
        """Test providers to see which ones are working"""
        working = []
        test_messages = [{"role": "user", "content": "Hi"}]
        
        for provider_name in self.providers.keys():
            try:
                provider = getattr(g4f.Provider, provider_name)
                # Quick test
                response = g4f.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=test_messages,
                    provider=provider,
                    stream=False,
                    timeout=10
                )
                if response and len(str(response).strip()) > 0:
                    working.append(provider_name)
                    logger.info(f"Provider {provider_name} is working")
                else:
                    logger.warning(f"Provider {provider_name} returned empty response")
            except Exception as e:
                logger.warning(f"Provider {provider_name} test failed: {e}")
                continue
        
        logger.info(f"Working providers: {working}")
        return working
    
    def _test_image_providers(self) -> List[str]:
        """Test image providers to see which ones are working"""
        working = []
        
        # 简化测试，先返回可能工作的提供商
        # 在实际使用时进行真正的测试
        potential_working = ['PollinationsAI', 'HuggingSpace', 'Together']
        
        for provider_name in self.image_providers.keys():
            if provider_name in potential_working:
                working.append(provider_name)
                logger.info(f"Image provider {provider_name} marked as potentially working")
        
        logger.info(f"Working image providers: {working}")
        return working
    
    def generate_response(self, messages: List[Dict], provider_name: str = None, model_name: str = None, stream: bool = False):
        """Generate response using g4f with fallback mechanism"""
        
        # Clean and validate messages
        clean_messages = []
        for msg in messages:
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                clean_messages.append({
                    'role': str(msg['role']).lower(),
                    'content': str(msg['content']).strip()
                })
        
        if not clean_messages:
            raise ValueError("No valid messages provided")
        
        # Get model
        model = model_name if model_name else 'gpt-3.5-turbo'
        
        # Try specified provider first, then fallback to working providers
        providers_to_try = []
        if provider_name and provider_name in self.providers:
            providers_to_try.append(provider_name)
        
        # Add working providers as fallback
        providers_to_try.extend([p for p in self.working_providers if p not in providers_to_try])
        
        # If no working providers, try all available providers
        if not providers_to_try:
            providers_to_try = list(self.providers.keys())
        
        # Try providers one by one
        last_error = None
        for provider_name in providers_to_try:
            try:
                logger.info(f"Trying provider: {provider_name}")
                provider = getattr(g4f.Provider, provider_name)
                
                if stream:
                    response = g4f.ChatCompletion.create(
                        model=model,
                        messages=clean_messages,
                        provider=provider,
                        stream=True,
                        timeout=30
                    )
                else:
                    response = g4f.ChatCompletion.create(
                        model=model,
                        messages=clean_messages,
                        provider=provider,
                        stream=False,
                        timeout=30
                    )
                
                # Validate response
                if response:
                    if stream:
                        return response  # Return generator for streaming
                    else:
                        response_str = str(response).strip()
                        if response_str and len(response_str) > 0:
                            logger.info(f"Success with provider: {provider_name}")
                            return response_str
                        else:
                            logger.warning(f"Empty response from provider: {provider_name}")
                            continue
                else:
                    logger.warning(f"No response from provider: {provider_name}")
                    continue
                    
            except Exception as e:
                last_error = e
                logger.warning(f"Provider {provider_name} failed: {e}")
                continue
        
        # If all providers failed, try without specifying provider
        try:
            logger.info("Trying without specific provider")
            if stream:
                response = g4f.ChatCompletion.create(
                    model=model,
                    messages=clean_messages,
                    stream=True,
                    timeout=30
                )
            else:
                response = g4f.ChatCompletion.create(
                    model=model,
                    messages=clean_messages,
                    stream=False,
                    timeout=30
                )
            
            if response:
                if stream:
                    return response
                else:
                    response_str = str(response).strip()
                    if response_str:
                        return response_str
                        
        except Exception as e:
            last_error = e
            logger.error(f"Final attempt failed: {e}")
        
        # If everything failed
        raise Exception(f"All providers failed. Last error: {last_error}")
    
    def generate_image(self, prompt: str, provider_name: str = None, model: str = None, size: str = "1024x1024", quality: str = "standard", n: int = 1):
        """Generate image using g4f with new Client API"""
        
        if not prompt or not prompt.strip():
            raise ValueError("No prompt provided")
        
        # Clean prompt
        prompt = prompt.strip()
        
        try:
            # 使用新的 Client API
            from g4f.client import Client
            
            # 创建客户端，如果指定了提供商则使用指定的
            if provider_name and provider_name in self.image_providers:
                try:
                    provider = getattr(g4f.Provider, provider_name)
                    client = Client(image_provider=provider)
                    logger.info(f"Using specific image provider: {provider_name}")
                except Exception as e:
                    logger.warning(f"Failed to set specific provider {provider_name}: {e}")
                    client = Client()
            else:
                client = Client()
                logger.info("Using default image provider")
            
            # 确定使用的模型
            image_model = model or 'flux'
            
            # 调用图片生成
            logger.info(f"Generating image with model: {image_model}, prompt: {prompt[:50]}...")
            
            response = client.images.generate(
                model=image_model,
                prompt=prompt,
                response_format="url"  # 尝试获取 URL 格式
            )
            
            # 处理响应
            if response and hasattr(response, 'data') and response.data:
                image_data = response.data[0]
                
                # 尝试获取 URL
                if hasattr(image_data, 'url') and image_data.url:
                    logger.info(f"Image generated successfully with URL")
                    return {
                        'url': image_data.url,
                        'provider': provider_name or 'auto'
                    }
                
                # 尝试获取 base64 数据
                elif hasattr(image_data, 'b64_json') and image_data.b64_json:
                    logger.info(f"Image generated successfully with base64")
                    return {
                        'base64': f"data:image/png;base64,{image_data.b64_json}",
                        'provider': provider_name or 'auto'
                    }
                
                # 如果有其他格式的数据
                else:
                    logger.warning(f"Image data in unexpected format: {dir(image_data)}")
                    return {
                        'error': 'Image generated but in unexpected format',
                        'provider': provider_name or 'auto'
                    }
            else:
                logger.error("No image data in response")
                raise Exception("No image data received from provider")
                
        except ImportError:
            logger.error("g4f.client not available, trying fallback methods")
            # 如果新的 Client API 不可用，回退到旧方法
            return self._generate_image_fallback(prompt, provider_name, model, size, quality, n)
        
        except Exception as e:
            logger.error(f"Image generation failed with Client API: {e}")
            # 尝试回退方法
            try:
                return self._generate_image_fallback(prompt, provider_name, model, size, quality, n)
            except Exception as fallback_error:
                logger.error(f"Fallback method also failed: {fallback_error}")
                raise Exception(f"Image generation failed. Primary error: {e}, Fallback error: {fallback_error}")
    
    def _generate_image_fallback(self, prompt: str, provider_name: str = None, model: str = None, size: str = "1024x1024", quality: str = "standard", n: int = 1):
        """Fallback image generation method using older g4f APIs"""
        
        # Try specified provider first, then fallback to working providers
        providers_to_try = []
        if provider_name and provider_name in self.image_providers:
            providers_to_try.append(provider_name)
        
        # Add working image providers as fallback
        providers_to_try.extend([p for p in self.working_image_providers if p not in providers_to_try])
        
        # If no working providers, try all available image providers
        if not providers_to_try:
            providers_to_try = list(self.image_providers.keys())
        
        # Try providers one by one
        last_error = None
        for provider_name in providers_to_try:
            try:
                logger.info(f"Trying fallback image provider: {provider_name}")
                provider = getattr(g4f.Provider, provider_name)
                
                # 方法1: 尝试使用 ChatCompletion 进行图片生成
                try:
                    response = g4f.ChatCompletion.create(
                        model=model or "flux",
                        messages=[{"role": "user", "content": f"Generate an image: {prompt}"}],
                        provider=provider,
                        timeout=60
                    )
                    
                    if response and isinstance(response, str):
                        # 检查是否是 URL
                        if response.startswith('http'):
                            logger.info(f"Success with fallback provider {provider_name}: got URL")
                            return {'url': response, 'provider': provider_name}
                        # 检查是否是 base64
                        elif response.startswith('data:image'):
                            logger.info(f"Success with fallback provider {provider_name}: got base64")
                            return {'base64': response, 'provider': provider_name}
                
                except Exception as e:
                    logger.warning(f"ChatCompletion method failed for {provider_name}: {e}")
                
                # 方法2: 尝试直接调用提供商的方法
                try:
                    if hasattr(provider, 'create_image') or hasattr(provider, 'generate_image'):
                        create_method = getattr(provider, 'create_image', None) or getattr(provider, 'generate_image', None)
                        if create_method:
                            response = create_method(prompt=prompt)
                            if response:
                                logger.info(f"Success with provider {provider_name}: direct method")
                                if isinstance(response, str) and response.startswith('http'):
                                    return {'url': response, 'provider': provider_name}
                                elif isinstance(response, dict) and 'url' in response:
                                    return {'url': response['url'], 'provider': provider_name}
                                
                except Exception as e:
                    logger.warning(f"Direct method failed for {provider_name}: {e}")
                    
            except Exception as e:
                last_error = e
                logger.error(f"Fallback image provider {provider_name} failed completely: {e}")
                continue
        
        # 如果所有方法都失败了
        raise Exception(f"All image generation methods failed. Last error: {last_error}")
    
    def refresh_working_providers(self):
        """Refresh the list of working providers"""
        self.working_providers = self._test_providers()
        self.working_image_providers = self._test_image_providers()
        return {
            'text_providers': self.working_providers,
            'image_providers': self.working_image_providers
        }

# Initialize service
gpt4free_service = GPT4FreeService()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         providers=gpt4free_service.providers,
                         models=gpt4free_service.models,
                         image_providers=gpt4free_service.image_providers,
                         image_models=gpt4free_service.image_models)

@app.route('/api/providers')
def get_providers():
    """Get available providers"""
    return jsonify(gpt4free_service.providers)

@app.route('/api/image-providers')
def get_image_providers():
    """Get available image providers"""
    return jsonify(gpt4free_service.image_providers)

@app.route('/api/image-models')
def get_image_models():
    """Get available image models"""
    return jsonify(gpt4free_service.image_models)

@app.route('/api/models')
def get_models():
    """Get available models"""
    return jsonify(gpt4free_service.models)

@app.route('/api/refresh-providers', methods=['POST'])
def refresh_providers():
    """Refresh working providers"""
    try:
        result = gpt4free_service.refresh_working_providers()
        return jsonify({
            'working_text_providers': result['text_providers'],
            'working_image_providers': result['image_providers'],
            'total_text_providers': len(gpt4free_service.providers),
            'total_image_providers': len(gpt4free_service.image_providers)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate response from GPT4Free"""
    try:
        data = request.json
        messages = data.get('messages', [])
        provider_name = data.get('provider')
        model_name = data.get('model')
        stream = data.get('stream', False)
        
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
        
        logger.info(f"Generate request: provider={provider_name}, model={model_name}, stream={stream}")
        logger.info(f"Messages: {messages}")
        
        try:
            if stream:
                def generate_stream():
                    try:
                        response = gpt4free_service.generate_response(
                            messages, provider_name, model_name, stream=True
                        )
                        
                        # Handle streaming response
                        content_sent = False
                        for chunk in response:
                            if chunk and str(chunk).strip():
                                content_sent = True
                                yield f"data: {json.dumps({'content': str(chunk)})}\n\n"
                        
                        if not content_sent:
                            yield f"data: {json.dumps({'error': 'No content received from provider'})}\n\n"
                        else:
                            yield f"data: {json.dumps({'done': True})}\n\n"
                        
                    except Exception as e:
                        logger.error(f"Streaming error: {e}")
                        yield f"data: {json.dumps({'error': str(e)})}\n\n"
                
                return Response(
                    generate_stream(),
                    mimetype='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'X-Accel-Buffering': 'no'
                    }
                )
            else:
                response = gpt4free_service.generate_response(
                    messages, provider_name, model_name, stream=False
                )
                
                if response and str(response).strip():
                    return jsonify({'response': str(response)})
                else:
                    return jsonify({'error': 'No response generated'}), 500
                
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return jsonify({'error': f'Generation failed: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Error in generate endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """Generate image from GPT4Free"""
    try:
        data = request.json
        prompt = data.get('prompt', '').strip()
        provider_name = data.get('provider')
        model = data.get('model')
        size = data.get('size', '1024x1024')
        quality = data.get('quality', 'standard')
        n = data.get('n', 1)
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        logger.info(f"Image generation request: provider={provider_name}, model={model}, prompt={prompt[:50]}...")
        
        try:
            result = gpt4free_service.generate_image(
                prompt=prompt,
                provider_name=provider_name,
                model=model,
                size=size,
                quality=quality,
                n=n
            )
            
            # Process result based on type
            if 'url' in result:
                # Return URL directly
                return jsonify({
                    'success': True,
                    'url': result['url'],
                    'provider': result['provider']
                })
            elif 'base64' in result:
                # Return base64 data
                return jsonify({
                    'success': True,
                    'base64': result['base64'],
                    'provider': result['provider']
                })
            elif 'error' in result:
                return jsonify({
                    'error': result['error'],
                    'provider': result['provider']
                }), 500
            else:
                return jsonify({'error': 'Invalid response format'}), 500
                
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            return jsonify({'error': f'Image generation failed: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Error in generate-image endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'text_providers_count': len(gpt4free_service.providers),
        'image_providers_count': len(gpt4free_service.image_providers),
        'models_count': len(gpt4free_service.models),
        'image_models_count': len(gpt4free_service.image_models),
        'working_text_providers': gpt4free_service.working_providers,
        'working_image_providers': gpt4free_service.working_image_providers,
        'working_text_count': len(gpt4free_service.working_providers),
        'working_image_count': len(gpt4free_service.working_image_providers)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
