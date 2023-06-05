/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */
import { html, TemplateResult } from 'lit';
import { customElement } from 'lit/decorators.js';
import { when } from 'lit/directives/when.js';
import { MobxLitElement } from '@adobe/lit-mobx';

// shared state
import { algonaut, algoX } from '../../state/modules/algonaut';

type HasAppIdArgs = {
  address: string;
  net: string;
  appId: number;
};

// fake server check
const addrHasAppId = async (args: HasAppIdArgs): Promise<boolean> => {
  console.log('addrHasAppId', args);

  // hardcoded for now
  args.net = 'testnet';

  const result = await algonaut.checkAppId(args.address, args.appId);
  console.log('result', result);
  return !!(result > 0);
};

const EL_NAME = 'a-appid-gated-comp';

@customElement(EL_NAME)
export default class CustomElement extends MobxLitElement {
  private algoX = algoX;

  hasAppId = false;
  appId = '';

  public override render(): TemplateResult {
    return html`
      <input
        .valueAsNumber=${this.appId}
        type="number"
        placeholder="Enter App ID"
        required
        @input=${(e: any) => this.appId = e.target.value}
      />
      <button @click=${this.doHasAppId} ?disabled=${!this.appId}>
        Check App ID
      </button>

      ${when(
        this.hasAppId,
        () => html`
          <p>👍</p>
        `,
        () => html`
          <p>👎</p>
        `
      )}
    `;
  }

  async doHasAppId() {
    console.log('doHasAppId');

    this.hasAppId = await addrHasAppId({
      net: 'testnet',
      address: this.algoX.address,
      appId: this.appId,
    });

    this.requestUpdate();
  }
}

declare global {
  interface HTMLElementTagNameMap {
    [EL_NAME]: CustomElement;
  }
}
