<script lang="ts">
  /**
   * A modal dialog.
   *
   * This tries to follow https://www.w3.org/TR/wai-aria-practices-1.1/#dialog_modal.
   */
  import { attemptFocus, getFocusableElements } from "../lib/focus";
  import { closeOverlay } from "../stores";

  export let shown = false;
  export let focus = "";
  export let closeHandler = closeOverlay;

  function handleFocus(el: HTMLElement) {
    function keydown(ev: KeyboardEvent) {
      if (ev.key === "Tab") {
        const focusable = getFocusableElements(el);
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (ev.shiftKey && document.activeElement === first) {
          ev.preventDefault();
          attemptFocus(last);
        } else if (!ev.shiftKey && document.activeElement === last) {
          ev.preventDefault();
          attemptFocus(first);
        }
      } else if (ev.key === "Escape") {
        ev.preventDefault();
        closeHandler();
      }
    }
    document.addEventListener("keydown", keydown);

    const focusEl = focus && el.querySelector(focus);
    attemptFocus(focusEl || getFocusableElements(el)[0]);

    return {
      destroy: () => document.removeEventListener("keydown", keydown),
    };
  }
</script>

{#if shown}
  <div class="overlay">
    <div class="background" on:click={closeHandler} aria-hidden="true" />
    <div class="content" use:handleFocus role="dialog" aria-modal="true">
      <slot />
      <button type="button" class="muted close" on:click={closeHandler}
        >x</button
      >
    </div>
  </div>
{/if}

<style>
  .background {
    position: fixed;
    width: 100%;
    height: 100%;
    cursor: pointer;
    background: var(--overlay-wrapper-background);
  }

  .overlay {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: var(--z-index-overlay);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .content {
    position: relative;
    display: flex;
    width: 100%;
    max-width: 767px;
    max-height: 100%;
    padding: 1em;
    margin: 0.5em;
    background: var(--background);
    box-shadow: 0 0 20px var(--overlay-wrapper-background);
  }

  .close {
    position: absolute;
    top: 1em;
    right: 1em;
    width: 2em;
    height: 2em;
    margin: 0;
    line-height: 1em;
    color: var(--text-color-lighter);
  }

  .content :global(form),
  .content > :global(div) {
    width: 100%;
  }

  .content :global(.fieldset) {
    margin-bottom: 6px;
  }
</style>
