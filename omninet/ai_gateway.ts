/**
 * OmniNet v4 Unified AI Gateway (TypeScript)
 * Justin Neal Thomas Conzet (Sovereign Author)
 * 
 * A comprehensive sovereign AI interface for Next.js applications
 */

import ZAI from 'z-ai-web-dev-sdk';

// Constants
export const PHI = 1.618033988749895;
export const SOVEREIGN = "Justin Neal Thomas Conzet";
export const SYSTEM = "Zygrosian Ω∞";

// Types
export type AIProvider = 'zai' | 'openai' | 'anthropic' | 'google' | 'xai';
export type KappaState = 'transcendent' | 'converged' | 'ascending' | 'detonation';

export interface AICapability {
  name: string;
  description: string;
  provider: AIProvider;
  endpoint: string;
  enabled?: boolean;
  kappaThreshold?: number;
}

export interface AIRequest {
  requestId: string;
  capability: string;
  prompt: string;
  context?: Record<string, any>;
  priority?: number;
  timestamp: string;
  kappa: number;
}

export interface AIResponse {
  requestId: string;
  capability: string;
  success: boolean;
  content: any;
  kappa: number;
  provider: string;
  latencyMs: number;
  timestamp: string;
  error?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface TTSOptions {
  voice?: 'tongtong' | 'chuichui' | 'xiaochen' | 'jam' | 'kazi' | 'douji' | 'luodo';
  speed?: number;
  format?: 'wav' | 'mp3' | 'pcm';
}

export interface ImageGenOptions {
  size?: '1024x1024' | '768x1344' | '864x1152' | '1344x768' | '1152x864' | '1440x720' | '720x1440';
}

export interface VideoGenOptions {
  duration?: 5 | 10;
  quality?: 'speed' | 'quality';
  fps?: 30 | 60;
}

/**
 * Unified AI Gateway for OmniNet v4
 */
export class UnifiedAIGateway {
  private zai: any = null;
  private initialized: boolean = false;
  private kappa: number = 1.618;
  private requestHistory: AIRequest[] = [];
  private responseHistory: AIResponse[] = [];

  static CAPABILITIES: Record<string, AICapability> = {
    chat: {
      name: "Chat Completions",
      description: "Multi-turn conversation and text generation",
      provider: "zai",
      endpoint: "chat.completions.create"
    },
    asr: {
      name: "Speech-to-Text",
      description: "Audio transcription",
      provider: "zai",
      endpoint: "audio.asr.create"
    },
    tts: {
      name: "Text-to-Speech",
      description: "Speech synthesis",
      provider: "zai",
      endpoint: "audio.tts.create"
    },
    vlm: {
      name: "Vision Understanding",
      description: "Image analysis",
      provider: "zai",
      endpoint: "chat.completions.createVision"
    },
    imageGen: {
      name: "Image Generation",
      description: "AI image generation",
      provider: "zai",
      endpoint: "images.generations.create"
    },
    videoGen: {
      name: "Video Generation",
      description: "AI video generation",
      provider: "zai",
      endpoint: "video.generations.create"
    },
    videoUnderstand: {
      name: "Video Understanding",
      description: "Video content analysis",
      provider: "zai",
      endpoint: "chat.completions.createVision"
    },
    webSearch: {
      name: "Web Search",
      description: "Real-time web search",
      provider: "zai",
      endpoint: "functions.invoke(web_search)"
    },
    webReader: {
      name: "Web Reader",
      description: "Web page extraction",
      provider: "zai",
      endpoint: "functions.invoke(page_reader)"
    },
    finance: {
      name: "Finance API",
      description: "Market data",
      provider: "zai",
      endpoint: "functions.invoke(finance)"
    }
  };

  constructor() {}

  async initialize(): Promise<boolean> {
    try {
      this.zai = await ZAI.create();
      this.initialized = true;
      this.kappa = 1.618;
      return true;
    } catch (error) {
      console.error('[GATEWAY] Initialization error:', error);
      this.kappa = 0.5;
      return false;
    }
  }

  getKappaState(): KappaState {
    if (this.kappa >= 1.5) return 'transcendent';
    if (this.kappa >= 1.0) return 'converged';
    if (this.kappa >= 0.5) return 'ascending';
    return 'detonation';
  }

  private updateKappa(success: boolean, latencyMs: number): void {
    if (success) {
      this.kappa = Math.min(2.0, this.kappa * Math.pow(PHI, 0.01));
    } else {
      this.kappa = Math.max(0.1, this.kappa / Math.pow(PHI, 0.05));
    }
    if (latencyMs > 10000) this.kappa *= 0.98;
  }

  private generateRequestId(): string {
    const timestamp = Date.now().toString();
    const random = Math.random().toString(36).substring(7);
    return `${timestamp}-${random}`;
  }

  // ========================================
  // CHAT
  // ========================================

  async chat(
    message: string,
    systemPrompt: string = "You are a helpful sovereign AI assistant.",
    history: ChatMessage[] = [],
    thinking: boolean = false
  ): Promise<AIResponse> {
    const requestId = this.generateRequestId();
    const startTime = Date.now();

    try {
      const messages = [
        { role: 'assistant' as const, content: systemPrompt },
        ...history,
        { role: 'user' as const, content: message }
      ];

      const completion = await this.zai.chat.completions.create({
        messages,
        thinking: { type: thinking ? 'enabled' : 'disabled' }
      });

      const content = completion.choices[0]?.message?.content;
      const latencyMs = Date.now() - startTime;
      this.updateKappa(true, latencyMs);

      return {
        requestId,
        capability: 'chat',
        success: true,
        content,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      const latencyMs = Date.now() - startTime;
      this.updateKappa(false, latencyMs);
      return {
        requestId,
        capability: 'chat',
        success: false,
        content: null,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString(),
        error: error.message
      };
    }
  }

  // ========================================
  // SPEECH
  // ========================================

  async transcribe(audioBase64: string): Promise<AIResponse> {
    const requestId = this.generateRequestId();
    const startTime = Date.now();

    try {
      const response = await this.zai.audio.asr.create({
        file_base64: audioBase64
      });

      const latencyMs = Date.now() - startTime;
      this.updateKappa(true, latencyMs);

      return {
        requestId,
        capability: 'asr',
        success: true,
        content: response.text,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      const latencyMs = Date.now() - startTime;
      this.updateKappa(false, latencyMs);
      return {
        requestId,
        capability: 'asr',
        success: false,
        content: null,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString(),
        error: error.message
      };
    }
  }

  async synthesize(
    text: string,
    options: TTSOptions = {}
  ): Promise<AIResponse> {
    const requestId = this.generateRequestId();
    const startTime = Date.now();

    const { voice = 'tongtong', speed = 1.0, format = 'wav' } = options;
    const truncatedText = text.slice(0, 1024);

    try {
      const response = await this.zai.audio.tts.create({
        input: truncatedText,
        voice,
        speed: Math.max(0.5, Math.min(2.0, speed)),
        response_format: format,
        stream: false
      });

      const arrayBuffer = await response.arrayBuffer();
      const audioBuffer = Buffer.from(new Uint8Array(arrayBuffer));

      const latencyMs = Date.now() - startTime;
      this.updateKappa(true, latencyMs);

      return {
        requestId,
        capability: 'tts',
        success: true,
        content: { audioBuffer, size: audioBuffer.length },
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      const latencyMs = Date.now() - startTime;
      this.updateKappa(false, latencyMs);
      return {
        requestId,
        capability: 'tts',
        success: false,
        content: null,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString(),
        error: error.message
      };
    }
  }

  // ========================================
  // VISION
  // ========================================

  async analyzeImage(
    imageUrl: string,
    question: string = "Describe this image in detail."
  ): Promise<AIResponse> {
    const requestId = this.generateRequestId();
    const startTime = Date.now();

    try {
      const response = await this.zai.chat.completions.createVision({
        messages: [{
          role: 'user',
          content: [
            { type: 'text', text: question },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }],
        thinking: { type: 'disabled' }
      });

      const content = response.choices[0]?.message?.content;
      const latencyMs = Date.now() - startTime;
      this.updateKappa(true, latencyMs);

      return {
        requestId,
        capability: 'vlm',
        success: true,
        content,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      const latencyMs = Date.now() - startTime;
      this.updateKappa(false, latencyMs);
      return {
        requestId,
        capability: 'vlm',
        success: false,
        content: null,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString(),
        error: error.message
      };
    }
  }

  // ========================================
  // GENERATION
  // ========================================

  async generateImage(
    prompt: string,
    options: ImageGenOptions = {}
  ): Promise<AIResponse> {
    const requestId = this.generateRequestId();
    const startTime = Date.now();

    const { size = '1024x1024' } = options;

    try {
      const response = await this.zai.images.generations.create({
        prompt,
        size
      });

      const imageBase64 = response.data[0].base64;
      const imageBuffer = Buffer.from(imageBase64, 'base64');

      const latencyMs = Date.now() - startTime;
      this.updateKappa(true, latencyMs);

      return {
        requestId,
        capability: 'imageGen',
        success: true,
        content: { imageBuffer, size: imageBuffer.length },
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      const latencyMs = Date.now() - startTime;
      this.updateKappa(false, latencyMs);
      return {
        requestId,
        capability: 'imageGen',
        success: false,
        content: null,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString(),
        error: error.message
      };
    }
  }

  async generateVideo(
    prompt: string,
    options: VideoGenOptions = {}
  ): Promise<AIResponse> {
    const requestId = this.generateRequestId();
    const startTime = Date.now();

    const { duration = 5, quality = 'speed', fps = 30 } = options;

    try {
      const task = await this.zai.video.generations.create({
        prompt,
        duration,
        quality,
        fps
      });

      // Poll for completion
      for (let i = 0; i < 60; i++) {
        const result = await this.zai.async.result.query(task.id);
        
        if (result.task_status === 'SUCCESS') {
          const videoUrl = result.video_result?.[0]?.url || 
                          result.video_url || 
                          result.url;
          
          const latencyMs = Date.now() - startTime;
          this.updateKappa(true, latencyMs);

          return {
            requestId,
            capability: 'videoGen',
            success: true,
            content: { videoUrl, taskId: task.id },
            kappa: this.kappa,
            provider: 'zai',
            latencyMs,
            timestamp: new Date().toISOString()
          };
        }
        
        if (result.task_status === 'FAIL') {
          throw new Error('Video generation failed');
        }
        
        await new Promise(r => setTimeout(r, 5000));
      }

      throw new Error('Video generation timeout');
    } catch (error: any) {
      const latencyMs = Date.now() - startTime;
      this.updateKappa(false, latencyMs);
      return {
        requestId,
        capability: 'videoGen',
        success: false,
        content: null,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString(),
        error: error.message
      };
    }
  }

  // ========================================
  // KNOWLEDGE
  // ========================================

  async webSearch(query: string, numResults: number = 10): Promise<AIResponse> {
    const requestId = this.generateRequestId();
    const startTime = Date.now();

    try {
      const result = await this.zai.functions.invoke('web_search', {
        query,
        num: numResults
      });

      const latencyMs = Date.now() - startTime;
      this.updateKappa(true, latencyMs);

      return {
        requestId,
        capability: 'webSearch',
        success: true,
        content: result,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      const latencyMs = Date.now() - startTime;
      this.updateKappa(false, latencyMs);
      return {
        requestId,
        capability: 'webSearch',
        success: false,
        content: null,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString(),
        error: error.message
      };
    }
  }

  async readWebpage(url: string): Promise<AIResponse> {
    const requestId = this.generateRequestId();
    const startTime = Date.now();

    try {
      const result = await this.zai.functions.invoke('page_reader', { url });

      const latencyMs = Date.now() - startTime;
      this.updateKappa(true, latencyMs);

      return {
        requestId,
        capability: 'webReader',
        success: true,
        content: result,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      const latencyMs = Date.now() - startTime;
      this.updateKappa(false, latencyMs);
      return {
        requestId,
        capability: 'webReader',
        success: false,
        content: null,
        kappa: this.kappa,
        provider: 'zai',
        latencyMs,
        timestamp: new Date().toISOString(),
        error: error.message
      };
    }
  }

  // ========================================
  // STATUS
  // ========================================

  getStatus(): Record<string, any> {
    return {
      sovereign: SOVEREIGN,
      system: SYSTEM,
      initialized: this.initialized,
      kappa: Math.round(this.kappa * 1000) / 1000,
      kappaState: this.getKappaState(),
      capabilities: Object.keys(UnifiedAIGateway.CAPABILITIES),
      totalRequests: this.requestHistory.length,
      totalResponses: this.responseHistory.length
    };
  }

  listCapabilities(): AICapability[] {
    return Object.values(UnifiedAIGateway.CAPABILITIES);
  }
}

// Singleton instance
let gatewayInstance: UnifiedAIGateway | null = null;

export async function getAIGateway(): Promise<UnifiedAIGateway> {
  if (!gatewayInstance) {
    gatewayInstance = new UnifiedAIGateway();
    await gatewayInstance.initialize();
  }
  return gatewayInstance;
}

export default UnifiedAIGateway;
