import shortid from 'shortid';

function* flatten(array, depth) {
  if (depth === undefined) {
    depth = 1;
  }
  for (const item of array) {
    if (Array.isArray(item) && depth > 0) {
      yield* flatten(item, depth - 1);
    } else {
      yield item;
    }
  }
}

class BasicObject {
  constructor(options = {}, schema = {}, placeholders = {}) {
    this.id = shortid.generate();
    schema.type = String();
    schema.name = String();
    Object.assign(this, schema);
    this.assign(options, placeholders);
  }

  assign(options = {}, placeholders = {}) {
    Object.assign(this,
      Object
        .keys(this)
        .filter((x) => {
          const assignType = typeof options[x];
          const selfType = typeof this[x];
          if (assignType === "undefined") {
            if (assignType !== "boolean" && !!this[x]) {
              return true;
            } else {
              this[x] = undefined;
            }
          } else if (assignType === "string") { // && options[x].substring(1, options[x].length-1) in placeholders) {
            return true;
          } else if (selfType !== assignType) {
            console.warn(`"${x}" assignment rejected :: ${selfType} <- ${assignType}`);
          }
          return selfType === assignType
        })
        .reduce((a, key) => {
          let ret = undefined;
          const x = options[key];
          if (typeof x === 'string' && x.substring(1, x.length - 1) in placeholders) {
            ret = placeholders[options[key].substring(1, options[key].length - 1)];
          } else {
            ret = options[key] || this[key]
          }

          return ({ ...a, [key]: ret })
        }, {})
    );
  }

  start(cb) {
    console.log(`[${self.name}] start`)

    if (this.duration && this.duration > 0) {
      const self = this
      setTimeout(() => {
        console.log(`[${self.name}] >>> next`)
        cb()
      }, this.duration)
    }
  }
}

const Order = Object.freeze({
  SEQUENTIAL: Symbol("sequential"),
  RANDOM: Symbol("random"),
});

const MediaType = Object.freeze({
  VIDEO: Symbol("video"),
  IMAGE: Symbol("image"),
  SOUND: Symbol("sound")
});

class Experiment extends BasicObject {
  constructor(options = {}) {
    super(options, {
      items: Array(),
      order: Order.SEQUENTIAL,
      config: Object(),
      lang: String(),
    }, options.placeholders);

    this.items = this.items.map((opt) => {
      switch (opt.type) {
        // for now experiment only accept sequence
        case "sequence":
          return new Sequence(opt, options.placeholders);

        case "intro":
          return new Intro(opt, options.placeholders);

        case "preconditions":
          return new Preconditions(opt, options.placeholders);

        case "closing":
          return new Closing(opt, options.placeholders);

        default:
      }
    });

    this.head = function () {
      return this.items.length === 0 ? false : this.items[0].head()
    }

    // this.flattenItem = [...flatten(this.items, Infinity)];
    this.flattenItem = [...flatten(this.items.map((x) => x instanceof Sequence ? x.flattenItem : x).filter(x => x !== undefined), Infinity)]

    console.log(this.flattenItem)
  }
}

class Sequence extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      items: Array(),
      duration: Number(),
      order: Order.SEQUENTIAL
    }, placeholders);

    const items = this.items.map((opt) => {
      let ret = undefined

      switch (opt.type) {
        // for now experiment only accept sequence
        case "instruction":
          ret = new Instruction(opt, placeholders);
          break;
        case "rating":
          ret = new Rating(opt, placeholders);
          break;
        case "composite-rating":
          ret = new CompositeRating(opt, placeholders);
          break;
        case "math":
          ret = new OpenQuestion(opt, placeholders);
          break;
        case "media":
          ret = new Media(opt, placeholders);
          break;
        case "marker":
          ret = new Marker(opt, placeholders);
          break;
        case "delay":
          ret = new Delay(opt, placeholders);
          break;
        case "slideshow":
          ret = new Slideshow(opt, placeholders);
          break;
        case "sequence":
          ret = new Sequence(opt, placeholders);
          break;
        case "intro":
          ret = new Intro(opt, placeholders);
          break;
        case "closing":
          ret = new Closing(opt, placeholders);
          break;
        case "quiz":
          ret = new Quiz(opt, placeholders);
          break;
        case "playlist":
          ret = new Playlist(opt, placeholders);
          break;
        default:
      }

      return ret;
    }).filter((x) => x !== undefined);

    this.items = items;

    this.head = () => {
      if (items.length === 0)
        return false;

      if (items[0].type === "sequence") {
        return items[0].head();
      } else {
        return items[0]
      }
    }

    // flatten
    this.flattenItem = [...flatten(this.items.map((x) => x instanceof Sequence ? x.flattenItem : x).filter(x => x !== undefined), Infinity)]

    // console.log(" >> ", this.flattenItem)
  }
}

// Form type
class Instruction extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      text: Object(),
      html: Object(),
      icon: String(),
      iconWidth: Number(),
      iconHeight: Number(),
      duration: Number(),
    }, placeholders);

    this.isVisual = true;
  }
}

class Rating extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      name: String(),
      block_name: String(),
      text: Object(),
      html: Object(),
      duration: Number(),
      min: Number(),
      max: Number(),
      min_description: Object(),
      max_description: Object(),
    }, placeholders);

    this.isVisual = true;
  }
}


class CompositeRating extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      name: String(),
      // block_name: String(),
      // text: Object(),
      // html: Object(),
      // duration: Number(),
      // min: Number(),
      // max: Number(),
      // min_description: Object(),
      // max_description: Object(),
      questions: Array(),
      items: Array()
    }, placeholders);

    this.isVisual = true;
  }
}
class Slideshow extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      items: Array(),
      order: Order.RANDOM,
      duration: Number(),
      durationPerItem: Number(),
      catalogue: Object(),
      cond: String(),
      condItems: Object(),
      getItems: Function()
    }, placeholders);

    this.isVisual = true;
  }
}

class Playlist extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      items: Array(),
      order: Order.RANDOM,
      duration: Number(),
      durationPerItem: Number(),
      catalogue: Object(),
      getItems: Function()
    }, placeholders);

    this.isVisual = true;
  }
}

class OpenQuestion extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      text: String(),
      html: String(),
      duration: Number(),
    }, placeholders);

    this.isVisual = true;
  }
}

class Quiz extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      text: String(),
      html: String(),
      items: Array(),
      duration: Number(),
      durationPerItem: Number(),
      isTutorial: Boolean()
    }, placeholders);

    this.isVisual = true;
  }
}

class Media extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      file: String(),
      duration: Number(),
      volume: Number(),
      cond: String(),
      condFile: Object(),
    }, placeholders);

    this.isVisual = false;

    if (typeof options.isVisual !== "undefined") {
      this.isVisual = options.isVisual;
    }
  }
}

class Marker extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      code: Number(),
    }, placeholders);

    this.isVisual = false;
  }
}

class Delay extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {}, placeholders);

    this.isVisual = false;
  }
}

class Intro extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      title: Object(),
      subtitle: Object(),
      text: Object(),
    }, placeholders);

    this.isVisual = true;
  }
}

class Closing extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      title: Object(),
      subtitle: Object(),
      text: Object(),
    }, placeholders);

    this.isVisual = true;
  }
}

class Preconditions extends BasicObject {
  constructor(options = {}, placeholders = {}) {
    super(options, {
      text: String(),
      items: Array()
    }, placeholders);

    this.isVisual = true;
  }
}

export default Experiment
export {
  Experiment,
  Intro,
  Closing,
  Preconditions,
  Sequence,
  Instruction,
  Rating,
  CompositeRating,
  OpenQuestion,
  Slideshow,
  Playlist,
  Quiz,
  Delay,
  MediaType
}