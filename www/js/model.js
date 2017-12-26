export class Topic {
  constructor(id, name) {
    this.id_ = id;
    this.name_ = name;
  }

  get id() {
    return this.id_;
  }

  get name() {
    return this.name_;
  }
}
