export class EvaluationContext {
  constructor(userId, attributes = {}) {
    if (!userId) {
      throw new Error("userId is required");
    }
    this.userId = String(userId);
    this.attributes = { ...attributes };
  }

  toApiUser() {
    return {
      id: this.userId,
      ...this.attributes,
    };
  }
}
