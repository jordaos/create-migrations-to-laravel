<?php

use App\Models\TableStructure;
use App\Models\TableStructureColumn;
use Illuminate\Database\Migrations\Migration;

class Insert[CLASSNAME] extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        $tableStructure = TableStructure::where('table_name', '[TABLE_NAME]')->first();

        [CREATES]
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        $tableStructure = TableStructure::where('table_name', '[TABLE_NAME]')->first();

        $itemToDelete = [ENTITY]::where([
            [INSERT_FIELDS]
        ])->first();

        $itemToDelete->delete();
    }
}
