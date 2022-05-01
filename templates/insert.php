<?php

use App\Models\[ENTITY];
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
        [ENTITY]::create([
            [INSERT_FIELDS]
        ]);
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        $itemToDelete = [ENTITY]::where([
            [INSERT_FIELDS]
        ])->first();

        $itemToDelete->delete();
    }
}
