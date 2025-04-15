import { Block, CodeBlock, parseRoot } from "codehike/blocks"
import { z } from "zod"
import { Pre, RawCode, highlight } from "codehike/code"
import {
  Selection,
  Selectable,
  SelectionProvider,
} from "codehike/utils/selection"
import Content from "./scrolling.mdx"
import Link from "next/link"
import { tokenTransitions } from "../components/annotations/token-transitions"

import { mark } from "../components/annotations/mark"
import { diff } from "../components//annotations/diff"
import { className } from "../components//annotations/classname"
import TableOfContents from "../components/tableofcontents"
import TableOfContentsItem from "../components/tableofcontentsitem"

import "../scrollycoding.css"

const Schema = Block.extend({
  intro: Block,
  steps: z.array(Block.extend({ code: CodeBlock })),
  outro: Block,
})

export default function Page() {
  const { intro, steps, outro } = parseRoot(Content, Schema)
  const makeLabel = (step: string | undefined) => {
    return (step) ? step.split(":")[0].trim() : "n/a"
  }
  const makeTopic = (step: string | undefined) => {
    return (step) ? step : "n/a"
  }
  return (
    <main className="scrollycoding">
      <TableOfContents />
      <Link href="/">Back to top</Link>
      <h1 className="mt-8">{intro.title}</h1>
      {intro.children}
      <SelectionProvider className="flex gap-4">
        {/* <div className="flex-1 mt-32 mb-[90vh] ml-2 prose prose-invert"> */}
        <div className="flex-1 mb-[90vh] prose prose-invert">
          {steps.map((step, i) => (
            <Selectable
              key={i}
              index={i}
              selectOn={["click", "scroll"]}
              className="border-l-4 border-zinc-700 data-[selected=true]:border-blue-400 px-5 py-2 mb-24 rounded bg-zinc-900"
            >
              <TableOfContentsItem topic={makeTopic(step.title)} label={makeLabel(step.title)}>
               <div>{step.children}</div>
              </TableOfContentsItem>
            </Selectable>
          ))}
        </div>
    {/* <div className="w-[40vw] max-w-xl bg-zinc-900"> */}
        <div className="max-w-7xl bg-zinc-900">
          <div className="top-4 sticky overflow-auto">
            <Selection
              from={steps.map((step, i) => (
                <Code codeblock={step.code} key={i}/>
              ))}
            />
          </div>
        </div>
      </SelectionProvider>
      <h2>{outro.title}</h2>
      {outro.children}
    </main>
  )
}

async function Code({ codeblock }: { codeblock: RawCode }) {
  const highlighted = await highlight(codeblock, "github-dark")
  return (
    <Pre
      code={highlighted}
      handlers={[tokenTransitions, mark, diff, className]}
      className="min-h-[40rem] bg-transparent"
    />
  )
}
