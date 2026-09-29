export const api = {
  async get(path: string) {
    // Mock API for demo - replace with real implementation
    console.log('[Mock API] GET', path);
    if (path === '/api/control-plane') {
      return { data: { missions: [], approvals: [], audit: [], learning: [], agents: [] } };
    }
    if (path === '/api/integrations') {
      return { data: { integrations: [] } };
    }
    if (path === '/api/profit/status') {
      return { data: { active: false, target: 200, currency: 'USD', next: 'Connect a real user and activate the profit mission.' } };
    }
    return { data: {} };
  },

  async post(path: string, body: any) {
    console.log('[Mock API] POST', path, body);
    if (path === '/api/actions') {
      return { data: { message: 'Action accepted (demo mode)', approval: null } };
    }
    if (path === '/api/approvals/decision') {
      return { data: { message: 'Decision recorded (demo mode)' } };
    }
    if (path === '/api/integrations/github/start' || path === '/api/integrations/orcid/start' || path === '/api/integrations/zenodo/start') {
      return { data: { authorizationUrl: '#' } };
    }
    if (path === '/api/sync/run') {
      return { data: { message: 'Sync completed (demo mode)' } };
    }
    if (path === '/api/profit/activate') {
      return { data: { active: true, target: body?.target || 200, currency: body?.currency || 'USD', startedAt: new Date().toISOString(), goalTitle: 'Verified profitable revenue', next: 'Research → Approve → Build → Sell → Attribute → Rank' } };
    }
    return { data: { message: 'OK (demo mode)' } };
  },

  async delete(path: string) {
    console.log('[Mock API] DELETE', path);
    return { data: { ok: true } };
  },
};

export const auth = {
  async signIn(options: any) {
    console.log('[Mock Auth] signIn', options);
    // Mock user
    return { user: { userId: 'demo-user', name: 'Demo CEO', email: 'demo@we-do-care.global' } };
  },

  async signOut() {
    console.log('[Mock Auth] signOut');
  },

  async getUser() {
    // Return mock user for demo
    return { userId: 'demo-user', name: 'Demo CEO', email: 'demo@we-do-care.global' };
  },

  isSignedIn() {
    return true;
  },
};

export const ws = {
  connect() {
    console.log('[Mock WS] connect');
    return {
      onMessage: (cb: any) => {},
      disconnect: () => {},
    };
  },
};