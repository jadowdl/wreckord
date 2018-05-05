import Links
import Record

CAT = Record.Record('CAT')
ANIMAL = Record.Record('ANIMAL')

Links.__LINKS[1].monkeyPatch()

CAT.kindOf(ANIMAL)
