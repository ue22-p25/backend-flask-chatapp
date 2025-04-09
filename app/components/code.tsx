import { Pre, RawCode, highlight } from "codehike/code"
import { mark } from "./annotations/mark"
import { diff } from "./annotations/diff"
import { className } from "./annotations/classname"
// import { callout } from "./annotations/callout"
// import { lineNumbers } from "./annotations/line-numbers"


export async function Code({ codeblock }: { codeblock: RawCode }) {
  const highlighted = await highlight(codeblock, "github-dark")
  return (
    <div className="px-4 bg-zinc-950 rounded">
      <div className="text-center text-zinc-400 text-lg font-semibold py-2">
        {highlighted.meta}
      </div>
      <Pre
        code={highlighted}
        // linenumbers make no sense in our context
        // and we're not using the callout handler yet
        // handlers={[callout, lineNumbers, mark, diff]}
        handlers={[mark, diff, className]}
        className="border border-zinc-800"
      />
    </div>
  )
}
